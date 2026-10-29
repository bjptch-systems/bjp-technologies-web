"""Default Privacy Policy text — the approved PDPC draft (Oct 2026).

Seeded into ``SiteSettings.privacy_policy_body`` and editable afterwards in
admin under Site Settings → Privacy Policy.
"""

DEFAULT_PRIVACY_POLICY = """
<p>BJP Technologies (T) Limited ("BJP", "we", "us") respects your privacy. This policy explains
what personal information we collect through bjptechnologies.co.tz, why we collect it, and the
choices you have. It follows the Personal Data Protection Act of Tanzania.</p>

<h2>1. Who we are</h2>
<p>BJP Technologies (T) Limited is an IT solutions company based in Msakuzi, Ubungo,
Dar es Salaam, Tanzania. Our contact details are in section 13.</p>

<h2>2. What we collect</h2>
<div class="privacy-table">
<table>
<thead><tr><th>When</th><th>What</th></tr></thead>
<tbody>
<tr><td>You fill in our contact form</td><td>Your first and last name, email address, phone
number (optional), company (optional), the service you are interested in, and your
message</td></tr>
<tr><td>You submit the contact form</td><td>Your IP address, the date and time, and a record
that you agreed to this policy</td></tr>
<tr><td>You accept cookies</td><td>How you use the website, such as pages visited, approximate
location (city or country), device and browser type. Collected by Google Analytics.</td></tr>
<tr><td>You visit any page</td><td>Your IP address is sent to Google when our fonts load, and
to our hosting provider in normal server logs</td></tr>
</tbody>
</table>
</div>
<p>We do not ask for sensitive information such as health, religion or financial account
details. Please do not include it in your message.</p>

<h2>3. Why we use it</h2>
<ul>
<li>To reply to your enquiry and give you the information or quote you asked for</li>
<li>To send you a confirmation that we received your message</li>
<li>To protect the website from spam and abuse. We use your IP address to limit repeated form
submissions.</li>
<li>To understand how visitors use the website and improve it, only if you accept analytics
cookies</li>
</ul>
<p>We use your contact details only for your enquiry. We do not add you to marketing lists
unless you ask us to, and we never sell your personal information.</p>

<h2>4. Your consent</h2>
<p>We collect contact form details only after you tick the consent box on the form. We use
analytics cookies and show the Google map only after you click "Accept" on the cookie banner.
You can withdraw consent at any time (see section 8).</p>

<h2>5. Cookies</h2>
<div class="privacy-table">
<table>
<thead><tr><th>Type</th><th>What it does</th><th>Needs consent?</th></tr></thead>
<tbody>
<tr><td>Essential</td><td>Keeps the contact form secure and remembers your cookie
choice</td><td>No. The website cannot work safely without them.</td></tr>
<tr><td>Analytics (Google Analytics)</td><td>Counts visits and shows which pages are
useful</td><td>Yes</td></tr>
<tr><td>Map (Google Maps)</td><td>Shows our office location on the Contact page. Google may set
its own cookies.</td><td>Yes</td></tr>
</tbody>
</table>
</div>
<p>You can change your choice at any time using the "Cookie settings" link at the bottom of
every page.</p>

<h2>6. Who we share it with</h2>
<ul>
<li><strong>Our email service provider</strong>, to deliver your enquiry to our team and send
your confirmation</li>
<li><strong>Google</strong>, for Google Analytics, Google Maps and Google Fonts, as described
above</li>
<li><strong>Our web hosting provider</strong>, which stores the website and its database</li>
<li><strong>Authorities</strong>, only when the law requires it</li>
</ul>
<p>Google may process data on servers outside Tanzania. Google applies its own safeguards to
protect that data.</p>

<h2>7. How long we keep it</h2>
<ul>
<li>Contact enquiries: up to 2 years after our last communication, then deleted</li>
<li>Analytics data: as set in our Google Analytics account, up to 14 months</li>
</ul>

<h2>8. Your rights</h2>
<p>You can ask us to:</p>
<ul>
<li>Tell you what personal information we hold about you and give you a copy</li>
<li>Correct information that is wrong or incomplete</li>
<li>Delete your information</li>
<li>Stop using your information, or withdraw your consent</li>
</ul>
<p>Email <a href="mailto:privacy@bjptechnologies.co.tz">privacy@bjptechnologies.co.tz</a> with
the subject "Privacy request". We will reply within 30 days. We may ask you to confirm your
identity first.</p>

<h2>9. How we protect it</h2>
<p>The website uses an encrypted (HTTPS) connection. Only authorised BJP staff can see contact
enquiries, through a password-protected admin panel.</p>

<h2>10. Children</h2>
<p>Our website is for businesses and organisations. We do not knowingly collect information
from children under 18.</p>

<h2>11. Complaints</h2>
<p>If you are unhappy with how we handle your information, contact us first so we can put it
right. You can also complain to the Personal Data Protection Commission (PDPC) of
Tanzania.</p>

<h2>12. Changes to this policy</h2>
<p>We may update this policy. The date at the top shows when it last changed.</p>

<h2>13. Contact us</h2>
<p>BJP Technologies (T) Ltd<br>
Email: <a href="mailto:privacy@bjptechnologies.co.tz">privacy@bjptechnologies.co.tz</a><br>
Phone: <a href="tel:+255764764011">0764 764 011</a><br>
Address: Msakuzi, Ubungo, Dar es Salaam, 16113, Tanzania<br>
Website: <a href="https://bjptechnologies.co.tz">bjptechnologies.co.tz</a></p>
""".strip()


def default_privacy_policy() -> str:
    return DEFAULT_PRIVACY_POLICY
