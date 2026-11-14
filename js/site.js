// Newsletter: no backend yet — open a prefilled e-mail so no address is lost.
// Swap this for your newsletter provider (Mailchimp, Brevo, …) when ready.
(function () {
  var form = document.querySelector('#newsletter form');
  if (!form) return;
  var input = form.querySelector('input[type="email"]');
  var button = form.querySelector('button');
  var note = document.createElement('p');
  note.className = 'form-note';
  form.appendChild(note);

  function submit(ev) {
    if (ev) ev.preventDefault();
    var email = (input.value || '').trim();
    if (!email || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
      note.textContent = 'Please enter a valid e-mail address.';
      note.className = 'form-note err';
      input.focus();
      return;
    }
    var subject = encodeURIComponent('Subscribe to The Animesy Magazine');
    var body = encodeURIComponent('Please add ' + email + ' to the magazine newsletter.');
    window.location.href = 'mailto:support@theanimesy.com?subject=' + subject + '&body=' + body;
    note.textContent = 'Thanks! Your e-mail app should open — just hit send.';
    note.className = 'form-note ok';
  }

  button.addEventListener('click', submit);
  form.addEventListener('submit', submit);
})();
