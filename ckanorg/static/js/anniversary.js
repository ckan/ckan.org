// ── Timeline ──
function tlToggle(trigger) {
    const item = trigger.parentElement;
    const wasOpen = item.classList.contains('open');
    document.querySelectorAll('.tl-item.open').forEach(el => el.classList.remove('open'));
    if (!wasOpen) item.classList.add('open');
}

// ── Global Reach counters ──
function grAnimCounter(el, target, dur) {
    const s = performance.now();
    const sfx = el.innerHTML.replace(/\d+/, '');
    function u(n) {
        const p = Math.min((n - s) / dur, 1);
        const e = 1 - Math.pow(1 - p, 3);
        el.innerHTML = Math.round(e * target) + sfx;
        if (p < 1) requestAnimationFrame(u);
    }
    requestAnimationFrame(u);
}
setTimeout(() => {
    grAnimCounter(document.getElementById('grC1'), 1000, 2000);
    grAnimCounter(document.getElementById('grC2'), 60, 1600);
    grAnimCounter(document.getElementById('grC3'), 6, 1200);
}, 300);

// ── Portal strips ──
const grRow1 = [
    {flag:'🇬🇧',d:'data.gov.uk',hot:true},{flag:'🇺🇸',d:'catalog.data.gov',hot:true},
    {flag:'🇨🇦',d:'open.canada.ca',hot:true},{flag:'🇦🇺',d:'data.gov.au',hot:true},
    {flag:'🇫🇷',d:'data.gouv.fr'},{flag:'🇩🇪',d:'govdata.de'},
    {flag:'🇮🇳',d:'data.gov.in'},{flag:'🇳🇿',d:'data.govt.nz'},
    {flag:'🇸🇬',d:'data.gov.sg'},{flag:'🇧🇷',d:'dados.gov.br'},
    {flag:'🇿🇦',d:'data.gov.za'},{flag:'🌐',d:'data.humdata.org',hot:true},
];
const grRow2 = [
    {flag:'🇨🇭',d:'opendata.swiss'},{flag:'🇮🇹',d:'dati.gov.it'},
    {flag:'🇪🇸',d:'datos.gob.es'},{flag:'🇳🇴',d:'data.norge.no'},
    {flag:'🇫🇮',d:'avoindata.fi'},{flag:'🇦🇹',d:'data.gv.at'},
    {flag:'🇰🇷',d:'data.go.kr'},{flag:'🇮🇪',d:'data.gov.ie'},
    {flag:'🇳🇱',d:'data.overheid.nl'},{flag:'🇦🇪',d:'bayanat.ae'},
    {flag:'🇲🇽',d:'datos.gob.mx'},{flag:'🇰🇪',d:'opendata.go.ke'},
];
function grMakeStrip(items) {
    const all = [...items, ...items, ...items, ...items];
    return all.map(i => `<span class="gr-sport${i.hot?' hot':''}"><span class="gr-sport-flag">${i.flag}</span>${i.d}</span>`).join('');
}
const grStripsEl = document.getElementById('grStrips');
if (grStripsEl) {
    grStripsEl.innerHTML = `<div class="gr-strip-row">${grMakeStrip(grRow1)}</div><div class="gr-strip-row">${grMakeStrip(grRow2)}</div>`;
}

// ── Stories published count ──
(function() {
    var published = document.querySelectorAll('.story-card:not(.soon)').length;
    var el = document.getElementById('publishedCount');
    if (el) el.textContent = published + ' published';
})();

// ── Stories filter ──
function storiesFilter(tag, btn) {
    document.querySelectorAll('.stories-filter .filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    document.querySelectorAll('.story-card').forEach(c => {
        c.style.display = (tag === 'all' || c.dataset.tag === tag) ? '' : 'none';
    });
}

// ── Form ──
function prefillStoryForm() {
    setTimeout(function() {
        var sel = document.querySelector('select[name="CKANUSE"]');
        if (sel) sel.value = 'contributor';
        var ta = document.querySelector('textarea[name="MESSAGE"]');
        if (ta) {
        ta.placeholder = 'Tell us your story — what has CKAN meant to you or your organisation?';
        }
    }, 400);
}


// Submitted in the background so the visitor stays on the form and only sees
// "Thank you" once the server has actually accepted the message. captcha.js
// fires this submit event after it has attached a fresh reCAPTCHA token.
// Without JS the form still posts normally and the page renders the result.
const joinForm = document.getElementById('joinForm');
if (joinForm) {
    const joinButton = document.getElementById('join-button');
    const joinError = document.getElementById('joinFormError');

    function showJoinError(message) {
        joinError.textContent = message;
        joinError.hidden = false;
        joinButton.disabled = false;
        // reCAPTCHA tokens are single-use: get a new one for the retry.
        if (typeof grecaptcha !== 'undefined' && typeof recaptchaWidgets !== 'undefined'
                && recaptchaWidgets.joinForm !== undefined) {
            grecaptcha.reset(recaptchaWidgets.joinForm);
        }
    }

    joinForm.addEventListener('submit', function (event) {
        event.preventDefault();
        joinButton.disabled = true;
        joinError.hidden = true;

        fetch(window.location.pathname, {
            method: 'POST',
            body: new FormData(joinForm),
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
            credentials: 'same-origin',
        })
            .then(function (response) {
                return response.json()
                    .catch(function () { return {}; })
                    .then(function (data) {
                        if (response.ok && data.ok) {
                            joinForm.closest('.involve-form').classList.add('is-sent');
                            return;
                        }
                        const captchaError = data.errors && data.errors.captcha;
                        showJoinError(captchaError
                            ? captchaError[0]
                            : 'Please check your name and email address and try again.');
                    });
            })
            .catch(function () {
                showJoinError('Your message could not be sent. Please check your connection and try again.');
            });
    });
}
