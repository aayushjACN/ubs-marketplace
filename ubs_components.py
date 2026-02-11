# ui_components.py
"""
Page UI components (CSS + render functions):
- Utilities (.full-bleed, .inner)
- Header
- Hero
- Services
- Footer

NOTE: render_chat_and_tabs() is intentionally NOT here.
"""
from __future__ import annotations

import streamlit as st

from assets import LOGO_URI, HERO_URI, CONTACT_ICON_URI, SEARCH_ICON_URI
from helpers import ubs_container

# --------------------------- Utilities CSS ---------------------------
APP_UTILS_CSS = """
.full-bleed{ width:100%; }
.inner{
  max-width:var(--grid-container-width);
  margin:0 auto;
  padding:0 var(--grid-container-spacing);
  box-sizing:content-box;
}
/* Full-bleed spacer (exact height) */
.section-spacer{
  display:block;
  width:100%;
  height: var(--spacer-size, var(--section-gap));   /* default from :root, overridable per call */
  background:#fff;
}

/* Align header rows and hero to the same rail (as in monolith) */
.header .toprow .inner,
.header .navrow .inner,
.hero .inner{
  max-width: var(--grid-container-width);
  margin-left: auto;
  margin-right: auto;
  padding-left: var(--grid-container-spacing);
  padding-right: var(--grid-container-spacing);
}
"""

# --------------------------- Header ---------------------------
HEADER_CSS = """
.header{background:#fff;border-bottom:1px solid #dedede;position:sticky;top:0;z-index:1000;}
.toprow .inner{height:64px;display:flex;align-items:center;justify-content:space-between;gap:24px;}
.leftpack{display:flex;align-items:center;gap:20px;white-space:nowrap;}
.logo{height:32px;display:block;}
.country{font-size:14px;color:#5a5d5c;}
.ctas{display:flex;align-items:center;gap:12px;}
.link, .link:link, .link:visited{color:#1c1c1c;text-decoration:none;font-size:13px;font-weight:400;}
.link:hover{text-decoration:underline;}
.action-icon{font-family:'ubs-icons';font-weight:300;display:inline-block;line-height:1;}
.btn-ghost, .btn-ghost:link, .btn-ghost:visited{color:#6b6f72;font-size:13px;text-decoration:none;}
.btn-ghost{display:inline-flex;align-items:center;gap:8px;padding:4px 10px;border:1px solid #6b6f72;border-radius:0;font-weight:400;}
.btn-ghost:hover{border-color:#52575a;color:#52575a;}
.btn-solid, .btn-solid:link, .btn-solid:visited{color:#fff !important;text-decoration:none;font-size:13px;}
.btn-solid{display:inline-flex;align-items:center;padding:4px 12px;background:var(--ubs-red);border-radius:0;font-weight:700;}

.navrow{position:relative;border-bottom:1px solid #e9e9e9;}
.navrow .inner{height:50px;display:flex;align-items:center;}
.nav{display:flex;align-items:center;}
.nav ul{display:flex;gap:40px;list-style:none;margin:0;padding:0;font-weight:400;font-size:16px;letter-spacing:.1px;}
.nav a{color:var(--ubs-gray-dark);text-decoration:none;}
.nav a:hover{color:var(--ubs-red);}
.search-inline{margin-left:auto;display:inline-flex;align-items:center;justify-content:center;width:32px;height:32px;border:none;background:transparent;padding:0;}
.search-inline img{width:18px;height:18px;}

/* kill UA indent completely (matches monolith) */
.nav { margin: 0; padding: 0; }
.nav ul {
  margin: 0; padding: 0;
  padding-inline-start: 0; margin-inline-start: 0; list-style: none;
}
.header .navrow .inner { padding-left: calc(var(--grid-container-spacing) + var(--nav-left-nudge)); }
.header .navrow nav,
.header .navrow .nav,
.header .navrow .nav ul{
  margin:0 !important; padding:0 !important;
  padding-inline-start:0 !important; margin-inline-start:0 !important; list-style:none !important;
}
.header .navrow .nav > ul > li{ margin:0 !important; padding:0 !important; }

.toprow .inner{
   height:64px;                           /* match original */
   display:flex; align-items:center; justify-content:space-between; gap:24px;
   flex-wrap:nowrap;                      /* present in original: prevents wrapping-induced height bumps */
 }
 .navrow .inner{
   height:50px;                           /* match original */
   display:flex; align-items:center;
 }

 /* size the SVG icons — present in original */
.btn-ghost .action-icon{ width:16px; height:16px; }
.search-inline img{ width:18px; height:18px; }
"""

def render_header(extra_nav_links: list[str] = None) -> None:
    extra_nav_links = extra_nav_links or []
    base_links = [
      "Wealth Management",
      "Asset Management",
      "Investment Bank",
      "About us",
      "Careers",
    ]
    all_links = base_links + list(extra_nav_links)
    nav_items_html = "\n          ".join(
        f"<li><a href='#'>{label}</a></li>" for label in all_links
    )

    st.markdown(
        f"""
<header class='full-bleed header'>
  <div class='toprow'>
    <div class='inner'>
      <div class='leftpack'>
        <img src='{LOGO_URI}' alt='UBS' class='logo'/>
        <span class='country'>United Kingdom</span>
      </div>
      <div class='ctas'>
        <a href='#' class='link'>Locations</a>
        <a href='#' class='btn-ghost'>
          <img src='{CONTACT_ICON_URI}' alt='' class='action-icon'/> Contact
        </a>
        <a href='#' class='btn-solid'>Client logins</a>
      </div>
    </div>
  </div>
  <div class='navrow'>
    <div class='inner'>
      <nav class='nav'>
        <ul>
          {nav_items_html}
        </ul>
      </nav>
      <button class='search-inline' aria-label='Search'>
        <img src='{SEARCH_ICON_URI}' alt='Search'/>
      </button>
    </div>
  </div>
</header>
""",
        unsafe_allow_html=True,
    )

# --------------------------- Hero ---------------------------
HERO_CSS = """
.hero{
  background-image:url('__HERO__');
  background-size:cover; background-position:center;
  min-height:540px; display:flex; align-items:center;
}

/* match monolith: hero inner rail uses width (not only max-width) and block */
.hero .inner{
  width: var(--grid-container-width);
  margin-left:auto; margin-right:auto;
  padding-left:var(--grid-container-spacing); padding-right:var(--grid-container-spacing);
  display:block;
}

.hero-card{
  position:relative; background:#fff; border:1px solid #e6e6e6; box-shadow:0 10px 20px rgba(0,0,0,.10);
  width: calc(var(--grid-absolute-col-width)*6 + var(--grid-absolute-gutter)*5);
  padding:48px 56px 56px var(--card-pad-left); margin-left:0;
}
.hero-copy{position:relative;}
.hero-card h2{font-size:44px;line-height:1.12;margin:0;font-weight:400;}
.hero-card h2 + p{margin-top:8px;}
.hero-card p{margin:0;font-size:24px;line-height:1.6;}
.hero-copy::before{
  content:""; position:absolute; left:calc(-1 * var(--stripe-offset));
  top:var(--stripe-top-adjust); bottom:var(--stripe-bottom-adjust);
  width:var(--stripe-width); background:var(--ubs-red);
}
.btn-primary{background:var(--ubs-red);color:#fff !important;padding:12px 22px;border-radius:0;font-size:16px;font-weight:700;text-decoration:none !important;display:inline-flex;align-items:center;gap:8px;margin-top:22px;margin-left:calc(-1 * var(--stripe-offset));}
.btn-primary .chev{width:18px;height:18px;display:inline-block;}
"""

HERO_CARD_HTML = """
<div class='hero-card'>
  <div class='hero-copy'>
    <h2>What's next for global wealth?</h2>
    <p>The world keeps getting richer, with 2024 seeing another surge in wealth according to our latest Global Wealth Report.</p>
  </div>
  <a href='#' class='btn-primary'>
    Explore more
    <svg class='chev' viewBox='0 0 16 16' aria-hidden='true' focusable='false'>
      <path d='M5 3l5 5-5 5' fill='none' stroke='currentColor' stroke-width='2'
            stroke-linecap='round' stroke-linejoin='round'/>
    </svg>
  </a>
</div>
""".strip()

def render_hero(
    header_text: str = "What's next for global wealth?",
    paragraph_text: str = "The world keeps getting richer, with 2024 seeing another surge in wealth according to our latest Global Wealth Report.",
    button_text: str = "Explore more",
) -> None:
    st.markdown(
        f"""
<section class='full-bleed hero'>
  <div class='inner'>
    <div class='hero-card'>
      <div class='hero-copy'>
        <h2>{header_text}</h2>
        <p>{paragraph_text}</p>
      </div>
      <a href='#' class='btn-primary'>
        {button_text}
        <svg class='chev' viewBox='0 0 16 16' aria-hidden='true' focusable='false'>
          <path d='M5 3l5 5-5 5' fill='none' stroke='currentColor' stroke-width='2'
                stroke-linecap='round' stroke-linejoin='round'/>
        </svg>
      </a>
    </div>
  </div>
</section>
""",
        unsafe_allow_html=True,
    )

# --------------------------- Services ---------------------------
SERVICES_CSS = """
.section.services-section{ background:var(--ubs-gray-light); }
.section.services-section .inner{
  max-width: var(--grid-container-width);
  margin-left:auto; margin-right:auto;
  padding-left:var(--grid-container-spacing); padding-right:var(--grid-container-spacing);
  padding-top:64px; padding-bottom:64px;
}
.section.services-section h2{
  font-weight:300; font-size:2.5rem; line-height:3rem; margin:0 0 2.5rem 0; color:var(--ubs-gray-dark);
}
.services{ display:grid; grid-template-columns:repeat(3, minmax(0, 1fr)); column-gap: calc(var(--grid-absolute-gutter) * 3); row-gap:40px; }
.service h3{ font-weight:300; font-size:24px; line-height:2.25rem; margin:0 0 10px 0; color:var(--ubs-black); }
.service p{ font-weight:300; font-size:16px; line-height:1.625rem; margin:0 0 16px 0; color:var(--ubs-black); }
.service a{ display:inline-flex; align-items:center; gap:8px; text-decoration:none; font-weight:700; color:var(--ubs-black); }
.service a .chev{ width:16px; height:16px; display:inline-block; stroke:var(--ubs-red); fill:none; stroke-width:2; stroke-linecap:round; stroke-linejoin:round; }

/* Ensure no text clamps override (monolith forces full width) */
.section.services-section .service h3,
.section.services-section .service p { max-width:none !important; }

/* Our services section keeps the gray background + white bands above/below */
.section.services-section{
  position: relative;
  background: var(--ubs-gray-light);
}

/* Force column headings and body copy to pure black (monolith) */
.section.services-section .service h3,
.section.services-section .service p { color: var(--ubs-black) !important; }
"""

SERVICES_HTML = """
<section class='full-bleed section services-section'>
  <div class='inner'>
    <h2>Our services</h2>
    <div class='services'>
      <div class='service'>
        <h3>Discover a clearer financial future</h3>
        <p>We offer you a total wealth solution, from wealth planning to investing to philanthropy.</p>
        <a href="#">Wealth Management
            <svg class="chev" viewBox="0 0 16 16" aria-hidden="true" focusable="false">
                <path d="M5 3l5 5-5 5"></path>
            </svg>
        </a>
      </div>
      <div class='service'>
        <h3>One of the world's leading asset managers</h3>
        <p>Offering a diverse range of traditional and alternative investment capabilities.</p>
        <a href="#">Asset Management
            <svg class="chev" viewBox="0 0 16 16" aria-hidden="true" focusable="false">
                <path d="M5 3l5 5-5 5"></path>
            </svg>
        </a>
      </div>
      <div class='service'>
        <h3>An Investment Bank focused on your needs</h3>
        <p>Through informed advice, tailored ideas and best-in-class execution.</p>
        <a href="#">Investment Bank
            <svg class="chev" viewBox="0 0 16 16" aria-hidden="true" focusable="false">
                <path d="M5 3l5 5-5 5"></path>
            </svg>
        </a>
      </div>
    </div>
  </div>
</section>
""".strip()

def render_services(
    section_header: str = "Our services",
    items: list[tuple[str, str, str]] = None,
) -> None:
    items = items or [
        (
            "Discover a clearer financial future",
            "We offer you a total wealth solution, from wealth planning to investing to philanthropy.",
            "Wealth Management",
        ),
        (
            "One of the world's leading asset managers",
            "Offering a diverse range of traditional and alternative investment capabilities.",
            "Asset Management",
        ),
        (
            "An Investment Bank focused on your needs",
            "Through informed advice, tailored ideas and best-in-class execution.",
            "Investment Bank",
        ),
    ]

    services_html = "\n".join(
        [
            f"""      <div class='service'>
        <h3>{h}</h3>
        <p>{p}</p>
        <a href="#">{link}
            <svg class="chev" viewBox="0 0 16 16" aria-hidden="true" focusable="false">
                <path d="M5 3l5 5-5 5"></path>
            </svg>
        </a>
      </div>"""
            for (h, p, link) in items
        ]
    )

    st.markdown(
        f"""
<section class='full-bleed section services-section'>
  <div class='inner'>
    <h2>{section_header}</h2>
    <div class='services'>
{services_html}
    </div>
  </div>
</section>
""",
        unsafe_allow_html=True,
    )

# --------------------------- Footer ---------------------------
FOOTER_CSS = """
.site-footer{ background:var(--ubs-gray-light); }
.footer-inner{ padding-top:48px; padding-bottom:32px; font-size:13px; color:#5a5d5c; }

/* centered tagline + greyed UBS logo */
.footer-top{
  display:flex; align-items:center; justify-content:center; gap:24px;
  padding:8px 0 28px;
}
.footer-top .purpose-text{
  margin:0; font-weight:300; font-size:20px; line-height:1.45;
  color:var(--ubs-gray-dark); max-width:460px; text-align:left;
}
.footer-top .footer-logo{
  height:36px; display:block;
  filter: grayscale(100%) brightness(0.55) contrast(1.05);
  opacity:.9;
}

.cols{ display:grid; grid-template-columns:repeat(4,1fr); gap:32px 48px; }
.cols h4{ margin:0 0 12px; font:700 14px/1 'FrutigerforUBSWeb',sans-serif; color:var(--ubs-gray-dark); }
.cols ul{ margin:0; padding:0; list-style:none; }
.cols li{ margin:0 0 10px; }
.cols a{ color:#6b6f72; text-decoration:none; }
.cols a:hover{ text-decoration:underline; color:var(--ubs-gray-dark); }

.change-domicile{ margin-top:18px; font-size:14px; color:var(--ubs-gray-dark); }
.change-domicile a{ font-weight:700; text-decoration:none; color:var(--ubs-gray-dark); margin-right:6px; }

.legal{ border-top:1px solid #e0ded6; margin-top:22px; padding-top:16px; font-size:12px; }
.legal-links{ color:var(--ubs-gray-dark); margin-bottom:10px; }
.legal-links a{ color:var(--ubs-gray-dark) !important; text-decoration:none; }
.legal-links a:hover{ text-decoration:underline; }
.legal-links .separator{ margin:0 6px; color:var(--ubs-gray-dark); }
.disclaimer{ color:#6b6f72; margin-bottom:8px; }
.copyright{ color:#6b6f72; }
"""

FOOTER_HTML = f"""
<div class='full-bleed site-footer'>
  <div class='inner footer-inner'>
    <div class='footer-top'>
      <p class='purpose-text'>Reimagining the power of investing.<br>Connecting people for a better world.</p>
      <img class='footer-logo' src='{LOGO_URI}' alt='UBS'>
    </div>
    <div class='cols'>
      <div>
        <h4>Capabilities</h4>
        <ul>
          <li><a href='#'>Wealth Management</a></li>
          <li><a href='#'>Asset Management</a></li>
          <li><a href='#'>Investment Bank</a></li>
        </ul>
      </div>
      <div>
        <h4>About us</h4>
        <ul>
          <li><a href='#'>About the UBS Group</a></li>
          <li><a href='#'>Latest media releases</a></li>
          <li><a href='#'>Investor Relations</a></li>
          <li><a href='#'>Sustainability and Impact</a></li>
          <li><a href='#'>Corporate governance</a></li>
          <li><a href='#'>Sponsoring</a></li>
          <li><a href='#'>Cyber Security at UBS</a></li>
        </ul>
      </div>
      <div>
        <h4>Careers at UBS</h4>
        <ul>
          <li><a href='#'>Overview</a></li>
          <li><a href='#'>About us</a></li>
          <li><a href='#'>Search jobs</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li><a href='#'>Global contacts</a></li>
          <li><a href='#'>Main offices</a></li>
          <li><a href='#'>Offices and contacts in the UK</a></li>
        </ul>
      </div>
    </div>
    <div class='change-domicile'><a href='#'>Change your domicile</a> <span>United Kingdom</span></div>
    <div class='legal'>
      <div class='legal-links'>
        <a href='#'>Information on UBS</a><span class='separator'>&bull;</span>
        <a href='#'>Terms of use</a><span class='separator'>&bull;</span>
        <a href='#'>Privacy statement</a><span class='separator'>&bull;</span>
        <a href='#'>Report fraudulent mail</a><span class='separator'>&bull;</span>
        <a href='#'>Additional legal information</a><span class='separator'>&bull;</span>
        <a href='#'>Privacy Settings</a>
      </div>
      <div class='disclaimer'>The products, services, information and/or materials contained within these web pages may not be available for residents of certain jurisdictions. Please consult the sales restrictions relating to the products or services in question for further information.</div>
      <div class='copyright'>© UBS 1998 – 2025. All rights reserved.</div>
    </div>
  </div>
</div>
""".strip()

def render_footer() -> None:
    st.markdown(FOOTER_HTML, unsafe_allow_html=True)

# --------------------------- Injection ---------------------------
def inject_app_css(hero_uri: str = HERO_URI) -> None:
    css = (
        APP_UTILS_CSS
        + HEADER_CSS
        + HERO_CSS.replace("__HERO__", hero_uri)
        + SERVICES_CSS
        + FOOTER_CSS
    )
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)