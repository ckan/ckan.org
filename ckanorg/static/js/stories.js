const STORIES = JSON.parse(document.getElementById('stories-data').textContent);

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
        '<div class="card-impact"><strong>' + s.impact[0].val + '</strong> ' + s.impact[0].label + '</div>' +
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
  var s = STORIES.find(function(x){ return x.id === id; });
  if (!s) return;
  currentIdx = STORIES.indexOf(s);
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
      return '<div class="impact-box"><div class="impact-n">' + i.val + '</div><div class="impact-l">' + i.label + '</div></div>';
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
  if (next >= 0 && next < STORIES.length) openReader(STORIES[next].id);
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

function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length === 2) return parts.pop().split(";").shift();
  return "";
}

async function submitNotify() {
  var input = document.getElementById("notifyEmail");
  var email = (input.value || "").trim();
  if (!email) return;

  var res = await fetch("/success-stories/notify/subscribe/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken")
    },
    body: JSON.stringify({ email: email })
  });

  if (!res.ok) return;

  document.getElementById("notifyForm").style.display = "none";
  document.getElementById("notifySuccess").style.display = "block";
}

document.getElementById('notifyEmail').addEventListener('keydown', function(e){
  if (e.key === 'Enter') submitNotify();
});

document.addEventListener('keydown', function(e){
  if (e.key === 'Escape') { closeReader(); closeNotify(); }
});

renderGrid('all');
