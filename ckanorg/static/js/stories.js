var STORIES = [
  {
    id: 0,
    org: 'UK Government',
    region: 'Europe',
    title: 'How data.gov.uk became the template for national open data',
    challenge: 'The UK Government needed to centralize and publish thousands of datasets from across hundreds of departments — consistently, at scale, and in a way citizens could actually use.',
    tags: ['gov'],
    color: '#ed5248',
    emoji: String.fromCodePoint(0x1F1EC, 0x1F1E7),
    meta: [
      { label: 'Portal', val: 'data.gov.uk' },
      { label: 'Launched', val: '2009' },
      { label: 'Datasets', val: '50,000+' }
    ],
    impact: [
      { n: '50,000', s: '+', label: 'Datasets published' },
      { n: '2009', s: '', label: 'Year launched' },
      { n: '#1', s: '', label: 'Ranked globally' }
    ],
    who: 'data.gov.uk is the UK Government\'s central open data portal, launched in 2009 under the Cabinet Office. It was one of the first national government portals in the world to go live, setting the standard for national open data infrastructure.',
    how: 'The UK chose CKAN because it was open source, battle-tested, and flexible enough to handle data from hundreds of publishing departments. CKAN\'s harvesting capabilities let individual department portals feed data automatically into the central catalog — solving the aggregation problem at scale.',
    outcome: 'data.gov.uk became a reference implementation for open government data worldwide. Dozens of national governments studied it before building their own portals, many of which also run on CKAN. It demonstrated that open source infrastructure could handle national-scale requirements.',
    quote: 'data.gov.uk showed that open source could work at national scale. Every government portal that came after learned from it.',
    quoteAuthor: 'Open Government Partnership, case review',
    portal: 'https://www.data.gov.uk'
  },
  {
    id: 1,
    org: 'US Federal Government',
    region: 'Americas',
    title: 'Migrating catalog.data.gov — a federal-scale challenge',
    challenge: 'The US Government needed to consolidate hundreds of thousands of federal datasets from agencies across the entire executive branch into a single, searchable, interoperable catalog.',
    tags: ['gov'],
    color: '#d4e5f1',
    emoji: String.fromCodePoint(0x1F1FA, 0x1F1F8),
    meta: [
      { label: 'Portal', val: 'catalog.data.gov' },
      { label: 'Migrated', val: '2013' },
      { label: 'Datasets', val: '300,000+' }
    ],
    impact: [
      { n: '300k', s: '+', label: 'Federal datasets' },
      { n: '100+', s: '', label: 'Contributing agencies' },
      { n: '2013', s: '', label: 'Migration year' }
    ],
    who: 'Data.gov is the United States Government\'s open data portal, managed by the General Services Administration (GSA). In 2013, the federal government undertook a major migration to rebuild Data.gov on CKAN following the CKAN 2.0 release.',
    how: 'CKAN\'s plugin architecture made it possible to meet the complex requirements of federal data publishing — from metadata standards compliance to agency-level access controls and automated harvesting from hundreds of separate agency systems.',
    outcome: 'The migration consolidated over 300,000 datasets from more than 100 federal agencies into a single searchable catalog. The extensions built for Data.gov have since been adopted by other national portals worldwide.',
    quote: 'The plugin architecture was a bet that the community would build things we hadn\'t thought of. The Data.gov migration proved that bet right.',
    quoteAuthor: 'Ian Ward, CKAN Lead Developer',
    portal: 'https://catalog.data.gov'
  },
  {
    id: 2,
    org: 'UN OCHA / HDX',
    region: 'Global',
    title: 'HDX: open humanitarian data when it matters most',
    challenge: 'During crises — earthquakes, conflict, disease outbreaks — humanitarian responders needed access to reliable, up-to-date data fast. That data existed across dozens of organisations but had no shared home.',
    tags: ['ngo'],
    color: '#eae65b',
    emoji: String.fromCodePoint(0x1F310),
    meta: [
      { label: 'Portal', val: 'data.humdata.org' },
      { label: 'Launched', val: '2014' },
      { label: 'Datasets', val: '20,000+' }
    ],
    impact: [
      { n: '20k', s: '+', label: 'Datasets available' },
      { n: '300+', s: '', label: 'Organisations' },
      { n: '250+', s: '', label: 'Crises covered' }
    ],
    who: 'The Humanitarian Data Exchange (HDX) is managed by the United Nations Office for the Coordination of Humanitarian Affairs (OCHA). It is the world\'s leading platform for sharing data across the humanitarian community in response to crises.',
    how: 'HDX is built on CKAN, extended with features designed specifically for humanitarian data: data quality checks, automated freshness indicators, private sharing for sensitive data, and integration with humanitarian metadata standards.',
    outcome: 'HDX now hosts over 20,000 datasets from more than 300 organisations, covering crises from the Syrian refugee emergency to COVID-19. During the 2015 Nepal earthquake, HDX was used by response teams within hours of the disaster.',
    quote: 'When a crisis hits, we need data in minutes, not weeks. HDX — built on CKAN — made that possible at scale across the entire humanitarian system.',
    quoteAuthor: 'OCHA Centre for Humanitarian Data',
    portal: 'https://data.humdata.org'
  },
  {
    id: 3,
    org: 'Government of Australia',
    region: 'Asia-Pacific',
    title: 'data.gov.au — federated open data across a continent',
    challenge: 'Australia\'s federal structure meant open data was scattered across Commonwealth, state, and territory governments — each with different systems, formats, and publishing cultures.',
    tags: ['gov'],
    color: '#ed5248',
    emoji: String.fromCodePoint(0x1F1E6, 0x1F1FA),
    meta: [
      { label: 'Portal', val: 'data.gov.au' },
      { label: 'Launched', val: '2013' },
      { label: 'Datasets', val: '30,000+' }
    ],
    impact: [
      { n: '30k', s: '+', label: 'Datasets' },
      { n: '8', s: '', label: 'States & territories' },
      { n: '2013', s: '', label: 'Launched' }
    ],
    who: 'data.gov.au is Australia\'s national open data portal, managed by the Digital Transformation Agency. It serves as the central discovery point for open data from Commonwealth, state, and territory governments.',
    how: 'CKAN\'s harvesting framework was the key. Rather than forcing agencies to migrate to a central system, data.gov.au harvests metadata from state and territory portals — many of which also run on CKAN — creating a federated catalog without a centralized publishing model.',
    outcome: 'data.gov.au became a model for federated open data infrastructure, demonstrating that you don\'t need centralized control to create a coherent national data catalog. Link Digital, now a CKAN co-steward, led much of this work.',
    quote: 'Federated harvesting meant we could give agencies autonomy while delivering a unified national catalog. CKAN made that architecture straightforward.',
    quoteAuthor: 'Steven De Costa, Link Digital / CKAN Co-Steward',
    portal: 'https://data.gov.au'
  },
  {
    id: 4,
    org: 'CKAN Community',
    region: 'Global',
    title: 'Building the ecosystem catalogue — mapping CKAN\'s global footprint',
    challenge: 'As the CKAN ecosystem grew to over 1,000 portals worldwide, there was no single place to discover what was out there — portals, extensions, datasets, and the organisations behind them.',
    tags: ['civic'],
    color: '#d4e5f1',
    emoji: String.fromCodePoint(0x1F5FA),
    meta: [
      { label: 'Portal', val: 'ecosystem.ckan.org' },
      { label: 'Launched', val: '2022' },
      { label: 'Sites indexed', val: '700+' }
    ],
    impact: [
      { n: '700', s: '+', label: 'Sites indexed' },
      { n: '1k', s: '+', label: 'Extensions' },
      { n: '60', s: '+', label: 'Countries' }
    ],
    who: 'ecosystem.ckan.org is a living catalog of CKAN-powered portals, extensions, and datasets maintained by the CKAN community. It is the discovery layer for the entire CKAN world.',
    how: 'Built on CKAN itself, the ecosystem catalog uses automated crawling, community contributions, and manual curation to maintain an accurate, up-to-date picture of the global CKAN landscape.',
    outcome: 'The ecosystem catalog has become the first port of call for anyone evaluating CKAN, looking for extensions, or wanting to understand what has been built before them. It surfaces the breadth of the community in a way that was previously invisible.',
    quote: 'Before the ecosystem catalog, the CKAN community was largely invisible to itself. Now we can see what we\'ve collectively built — and it\'s remarkable.',
    quoteAuthor: 'CKAN Stewardship Team',
    portal: 'https://ecosystem.ckan.org'
  },
  {
    id: 5,
    org: 'Government of Canada',
    region: 'Americas',
    title: 'open.canada.ca — bilingual open data at national scale',
    challenge: 'Canada needed a national open data portal that served both official languages, integrated with legacy departmental systems, and met strict federal accessibility and security requirements.',
    tags: ['gov'],
    color: '#eae65b',
    emoji: String.fromCodePoint(0x1F1E8, 0x1F1E6),
    meta: [
      { label: 'Portal', val: 'open.canada.ca' },
      { label: 'Launched', val: '2013' },
      { label: 'Datasets', val: '90,000+' }
    ],
    impact: [
      { n: '90k', s: '+', label: 'Datasets published' },
      { n: '2', s: '', label: 'Official languages' },
      { n: '100+', s: '', label: 'Federal departments' }
    ],
    who: 'open.canada.ca is Canada\'s national open government portal, maintained by Treasury Board of Canada Secretariat. It covers open data, open information, and open dialogue across the federal government.',
    how: 'Canada extended CKAN with full bilingual support for English and French across all metadata, search, and interface elements. Harvesting pipelines were built to ingest data from departmental systems automatically.',
    outcome: 'open.canada.ca hosts over 90,000 datasets and serves more than 100 federal departments. Its bilingual CKAN extensions have been shared back with the community and adapted by other multilingual portals.',
    quote: 'Building full bilingual support into CKAN was hard. Doing it in the open, as a contribution back to the community, made it worthwhile.',
    quoteAuthor: 'Treasury Board of Canada Secretariat',
    portal: 'https://open.canada.ca'
  }
];

var TAG_MAP = {
  gov:      { cls: 'tag-gov',      label: 'Government' },
  ngo:      { cls: 'tag-ngo',      label: 'NGO / Humanitarian' },
  research: { cls: 'tag-research', label: 'Research' },
  civic:    { cls: 'tag-civic',    label: 'Civic tech' },
  health:   { cls: 'tag-health',   label: 'Health' }
};

function renderGrid(filter) {
  var items = filter === 'all' ? STORIES : STORIES.filter(function(s){ return s.tags.indexOf(filter) > -1; });
  document.getElementById('countLabel').textContent = items.length;
  document.getElementById('storiesGrid').innerHTML = items.map(function(s) {
    var tagsHtml = s.tags.map(function(t){ return '<span class="tag ' + TAG_MAP[t].cls + '">' + TAG_MAP[t].label + '</span>'; }).join('');
    return '<a class="story-card" href="#" onclick="openReader(' + s.id + '); return false;">' +
      '<div class="card-header" style="background:' + s.color + ';">' +
        '<div class="card-header-bg">' + s.emoji + '</div>' +
        '<div class="card-region">' + s.region + '</div>' +
      '</div>' +
      '<div class="card-body">' +
        '<div class="card-org">' + s.org + '</div>' +
        '<div class="card-title">' + s.title + '</div>' +
        '<div class="card-challenge">' + s.challenge + '</div>' +
        '<div class="card-tags">' + tagsHtml + '</div>' +
      '</div>' +
      '<div class="card-footer">' +
        '<div class="card-impact"><strong>' + s.impact[0].n + s.impact[0].s + '</strong> ' + s.impact[0].label + '</div>' +
        '<span class="card-arrow">&#8594;</span>' +
      '</div>' +
    '</a>';
  }).join('');
}

function filterBy(tag, btn) {
  document.querySelectorAll('.filters-bar .filter-btn').forEach(function(b){ b.classList.remove('active'); });
  btn.classList.add('active');
  renderGrid(tag);
}

var currentIdx = 0;

function openReader(id) {
  currentIdx = id;
  var s = STORIES[id];
  document.getElementById('rBand').style.background = s.color;
  var onDark = s.color === '#ed5248';
  document.getElementById('rOrg').style.color = onDark ? 'rgba(255,255,255,0.6)' : 'rgba(0,0,0,0.45)';
  document.getElementById('rTitle').style.color = onDark ? 'rgba(255,255,255,0.9)' : 'rgba(0,0,0,0.85)';
  var rc = document.getElementById('readerPanel').querySelector('.reader-close');
  rc.style.background = onDark ? 'rgba(255,255,255,0.15)' : 'rgba(0,0,0,0.1)';
  rc.style.color = onDark ? 'rgba(255,255,255,0.7)' : 'rgba(0,0,0,0.5)';
  document.getElementById('rBandBg').textContent = s.emoji;
  document.getElementById('rOrg').textContent = s.org;
  document.getElementById('rTitle').textContent = s.title;
  document.getElementById('rMeta').innerHTML = s.meta.map(function(m){
    return '<div class="reader-meta-item"><div class="reader-meta-label">' + m.label + '</div><div class="reader-meta-val">' + m.val + '</div></div>';
  }).join('');
  document.getElementById('rContent').innerHTML =
    '<h3>Who they are</h3><p>' + s.who + '</p>' +
    '<h3>The challenge</h3><p>' + s.challenge + '</p>' +
    '<h3>How CKAN solved it</h3><p>' + s.how + '</p>' +
    '<h3>Impact &amp; outcomes</h3>' +
    '<div class="impact-row">' + s.impact.map(function(i){
      return '<div class="impact-box"><div class="impact-n">' + i.n + '<em>' + i.s + '</em></div><div class="impact-l">' + i.label + '</div></div>';
    }).join('') + '</div>' +
    '<p>' + s.outcome + '</p>' +
    '<div class="reader-quote"><p>' + s.quote + '</p><cite>' + s.quoteAuthor + '</cite></div>' +
    '<h3>Portal</h3>' +
    '<a href="' + s.portal + '" target="_blank" class="reader-portal-link">&#x1F310; ' + s.portal.replace('https://','') + ' &#x2197;</a>';
  document.getElementById('rPrev').disabled = id === 0;
  document.getElementById('rNext').disabled = id === STORIES.length - 1;
  document.getElementById('readerOverlay').classList.add('open');
  document.body.style.overflow = 'hidden';
  document.getElementById('readerPanel').scrollTop = 0;
}

function closeReader() {
  document.getElementById('readerOverlay').classList.remove('open');
  document.body.style.overflow = '';
}

function overlayBgClose(e) {
  if (e.target === document.getElementById('readerOverlay')) closeReader();
}

function navReader(dir) {
  var next = currentIdx + dir;
  if (next >= 0 && next < STORIES.length) openReader(next);
}

function openNotify() {
  document.getElementById('notifyOverlay').classList.add('open');
  document.body.style.overflow = 'hidden';
  setTimeout(function(){ document.getElementById('notifyEmail').focus(); }, 350);
}

function closeNotify() {
  document.getElementById('notifyOverlay').classList.remove('open');
  document.body.style.overflow = '';
}

function notifyBgClose(e) {
  if (e.target === document.getElementById('notifyOverlay')) closeNotify();
}

function submitNotify() {
  var email = document.getElementById('notifyEmail').value.trim();
  if (!email || email.indexOf('@') === -1) {
    document.getElementById('notifyEmail').style.borderColor = 'var(--red)';
    return;
  }
  document.getElementById('notifyForm').style.display = 'none';
  document.getElementById('notifySuccess').style.display = 'block';
}

document.getElementById('notifyEmail').addEventListener('keydown', function(e){
  if (e.key === 'Enter') submitNotify();
});

document.addEventListener('keydown', function(e){
  if (e.key === 'Escape') { closeReader(); closeNotify(); }
});

renderGrid('all');
