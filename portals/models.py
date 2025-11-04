import folium
import requests
from folium import plugins
from numerize import numerize

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel

from django.core.cache import cache
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_GET






class OpenDataPortalPage(Page):
    parent_page_types = ["home.HomePage"]

    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    class Meta:
        verbose_name = "Open Data Portal Page"
        verbose_name_plural = "Open Data Portal Pages"

    @staticmethod
    def get_autocomplete_suggestions(query):
        """Return autocomplete suggestions for portals matching the query."""
        portals = cache.get("open_data_portals", [])
        query = query.lower()
        suggestions = []

        for portal in portals:
            site_info = portal.get("SiteInfo", {})
            site_title = site_info.get("site_title", "")
            site_description = site_info.get("site_description", "")
            portal_country = portal.get("Coordinates", {}).get("country_name", "") or "Unknown"
            if query in site_title.lower():
                suggestions.append(
                    {
                        "label": site_title or site_description,
                        "value": site_title,
                        "description": site_description,
                        "country": portal_country,
                        "url": portal.get("Href", ""),
                    }
                )

        # Sort by number of datasets and limit to top 10
        suggestions = sorted(suggestions, key=lambda x: x["country"])
        return suggestions

    @staticmethod
    @require_GET
    def autocomplete_view(request):
        """AJAX view for autocomplete suggestions."""
        query = request.GET.get('term', '').strip()

        if not query:
            return JsonResponse([], safe=False)

        suggestions = OpenDataPortalPage.get_autocomplete_suggestions(query)
        return JsonResponse(suggestions, safe=False)

    def serve(self, request):
        query = request.GET.get("q", "")
        sort = request.GET.get("sort", "datasets")
        page_number = request.GET.get("page", 1)

        # Cache portals data for 1 hour
        portals = cache.get("open_data_portals")
        if not portals:
            response = requests.get("https://datashades.info/api/portal/list-filtered")
            portals = response.json() if response.status_code == 200 else []
            cache.set("open_data_portals", portals, 3600)

        # Statistics
        stats = {
            "total_portals": self.numtostr(len(portals)),
            "total_datasets": self.numtostr(sum(
                p.get("DatasetsNumber", 0)
                for p in portals if isinstance(p.get("DatasetsNumber"), int)
            )),
            "total_resources": self.numtostr(sum(
                p.get("ResourcesNumber", 0)
                for p in portals if isinstance(p.get("ResourcesNumber"), int)
            )),
            "total_users": self.numtostr(sum(
                p.get("UsersNumber", 0)
                for p in portals if isinstance(p.get("UsersNumber"), int)
            )),
        }

        # Search portals by name
        if query:
            portals = [
                p for p in portals
                if query.lower() in p.get("SiteInfo", {}).get("site_title", "").lower()
            ]

        # Sort portals based on the selected criteria
        if sort == "datasets":
            portals.sort(
                key=lambda x: x.get("DatasetsNumber", 0)
                if isinstance(x.get("DatasetsNumber"), int) else 0,
                reverse=True,
            )
        elif sort == "users":
            portals.sort(
                key=lambda x: x.get("UsersNumber", 0)
                if isinstance(x.get("UsersNumber"), int) else 0,
                reverse=True
            )
        elif sort == "resources":
            portals.sort(
                key=lambda x: x.get("ResourcesNumber", 0)
                if isinstance(x.get("ResourcesNumber"), int) else 0,
                reverse=True
            )
        elif sort == "name_asc":
            portals.sort(
                key=lambda x: x.get("SiteInfo", {}).get("site_title", "").lower()
            )
        elif sort == "name_desc":
            portals.sort(
                key=lambda x: x.get("SiteInfo", {}).get("site_title", "").lower(),
                reverse=True
            )

        # Paginate results
        paginator = Paginator(portals, 10)
        page_obj = paginator.get_page(page_number)

        # Generate the map using all portals (not just the paginated ones)
        map_html = self.generate_map(portals)

        return render(request, "portals/page.html", {
            "page": self,
            "query": query,
            "sort": sort,
            "portals": page_obj.object_list,
            "stats": stats,
            "page_obj": page_obj,
            "map_html": map_html,
        })

    def generate_map(self, portals):
        """Generate a Folium map with portal locations."""
        # Create a base map centered at a default location
        m = folium.Map(
            location=[0, 0],  # Default center
            zoom_start=2,
            tiles="CartoDB positron",  # Clean, light style map
            min_zoom=2,
        )
        
        # Create a marker cluster
        marker_cluster = plugins.MarkerCluster(
            name="Open Data Portals",
            overlay=True,
            control=True,
            icon_create_function="""
                function(cluster) {
                    var count = cluster.getChildCount();
                    var color = '#73B3D3';
                    if (count <= 10) {
                        color = '#73B3D3'; // blue
                    } else if (count <= 100) {
                        color = '#FAE159'; // yellow/gold
                    } else {
                        color = '#80CC72'; // green
                    }
                    return L.divIcon({
                        html: '<div style="background-color: ' + color + '; color: white; border-radius: 50%; width: 40px; height: 40px; line-height: 40px; text-align: center;">' + count + '</div>',
                        className: 'marker-cluster',
                        iconSize: L.point(40, 40)
                    });
                }
            """
        ).add_to(m)

        # Add markers for each portal
        for portal in portals:
            coordinates = portal.get("Coordinates", {})
            site_info = portal.get("SiteInfo", {})
            if coordinates.get("lat") and coordinates.get("lng"):
                try:
                    lat = float(coordinates["lat"])
                    lon = float(coordinates["lng"])

                    # Create popup content
                    popup_content = f"""
                        <div style="width: 250px">
                            <h4>{site_info.get("site_title", "Unknown Portal")}</h4>
                            <p><strong>Datasets:</strong> {portal.get('DatasetsNumber', 0)}</p>
                            <p><strong>Resources:</strong> {portal.get('ResourcesNumber', 0)}</p>
                            <p><strong>Users:</strong> {portal.get('UsersNumber', 0)}</p>
                            <a href="{portal.get('Href', '#')}" target="_blank" class="btn btn-md btn-visit" style="padding: 0;">
                            Visit Portal</a>
                        </div>
                    """

                    # Add marker to cluster
                    folium.Marker(
                        location=[lat, lon],
                        popup=folium.Popup(popup_content, max_width=300),
                    ).add_to(marker_cluster)
                except (ValueError, TypeError):
                    continue

        # Add fullscreen control
        plugins.Fullscreen().add_to(m)

        # Add layer control
        folium.LayerControl().add_to(m)

        # Return the HTML representation of the map
        return mark_safe(m._repr_html_())

    def numtostr(self, value):
        """Convert a number to a human-readable string format."""
        return numerize.numerize(value, 1)
