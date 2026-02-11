# streamlit_css.py
"""
Streamlit-specific CSS (auto-applies to Streamlit widgets only):
- Global reset & tokens
- Typography baseline
- st.title / st.header underline
- st.tabs polish
- st.chat_input polish
- st.container helpers used by the chat band/rail
"""
import streamlit as st
from assets import fontface_blocks

# 4a) Global reset + tokens (expanded to match monolith)
STREAMLIT_CSS_GLOBAL = """
#MainMenu, [data-testid="stHeader"], div[data-testid="stFooter"] { display:none !important; }
html, body, .stApp { background:#ffffff !important; width:100%; overflow-x:hidden; }

/* 🔒 Lock the root size to match the monolith/browsers (16px) */
html {
   font-size: 16px !important;             /* lock 1rem = 16px */
   -webkit-text-size-adjust: 100% !important;
   text-size-adjust: 100% !important;
}

.appview-container .main .block-container,
[data-testid="stAppViewContainer"] .main .block-container,
.block-container { padding:0 !important; margin:0 !important; max-width:100% !important; }

:root{
  --ubs-red:#e60000; --ubs-black:#000; --ubs-gray-dark:#1c1c1c; --ubs-gray:#5a5d5c; --ubs-gray-light:#f4f3ee;

  /* Grid & container math */
  --root-width:100vw;
  --grid-absolute-cols:12;
  --grid-absolute-gutter:20px;
  --grid-container-spacing:20px;
  --grid-container-max-width-xl:1290px;
  --grid-container-width: calc(var(--root-width) - var(--grid-container-spacing)*2);
  --grid-absolute-col-width: calc(
    (var(--grid-container-width) - var(--grid-absolute-gutter) * (var(--grid-absolute-cols) - 1))
    / var(--grid-absolute-cols)
  );
  --container: calc(var(--grid-container-width) + var(--grid-container-spacing) * 2);

  /* Rails / tweaks used in your monolith */
  --rail-left-offset: calc(var(--grid-absolute-col-width) * 1 + var(--grid-absolute-gutter) * 1);
  --nav-left-nudge: 0px;

  /* Hero internals (monolith) */
  --card-pad-left:72px;
  --stripe-offset:28px;
  --stripe-width:4px;
  --stripe-top-adjust:24px;
  --stripe-bottom-adjust:8px;

  /* Section spacing */
  /* canonical white band used by spacers (tune this ONE value) */
  --section-gap:32px;    /* visually matches your original; change to taste */
  /* keep compatibility if any old CSS still references services-spacer */
  --services-spacer: var(--section-gap);
}

@media(min-width:768px){  :root{ --grid-container-spacing:34px; } }
@media(min-width:1024px){ :root{ --grid-absolute-gutter:24px; --grid-container-spacing:42px; } }
@media(min-width:1280px){ :root{ --grid-absolute-gutter:40px; --grid-container-spacing:64px; } }
@media(min-width:1440px){
  :root{
    --grid-container-spacing:75px;
    --grid-container-width: min(calc(var(--root-width) - var(--grid-container-spacing)*2),1290px);
  }
}

/* Remove Streamlit's default vertical spacing between top-level blocks */
[data-testid="stVerticalBlock"]{
  gap: 0 !important;
}

header.header,
.navrow,
.toprow,
.hero{
  margin: 0 !important;
}

/* Remove any UA or wrapper margins that could add stray bands */
section, header, footer { margin: 0; }
.section.services-section { margin: 0 !important; }
.section-spacer { margin: 0 !important; }

/* Streamlit wrappers sometimes add spacing: pin to zero for blocks containing services/spacer */
[data-testid="stVerticalBlock"] { gap: 0 !important; }

/* Hard zero any margins that could create hairline bands */
section, header, footer { margin: 0; }
.section.services-section { margin: 0 !important; }
.section-spacer { margin: 0 !important; }

/* Streamlit wrappers: kill vertical gaps around our blocks */
[data-testid="stVerticalBlock"]{ gap: 0 !important; }

/* Ensure chat band doesn’t introduce any separator lines */
.st-key-chat_band{
  background:var(--ubs-gray-light);
  padding:32px 0;
  margin:0 !important;                 /* ensure no extra gap above */
  border:0 !important;                 /* prevent hairline separators */
}

/* Make spacers render at exact height (remove wrapper margins/line-height) */
[data-testid="stMarkdownContainer"]:has(> .section-spacer){
  margin:0 !important;
  padding:0 !important;
  line-height:0 !important;
}
[data-testid="stMarkdownContainer"] > .section-spacer{
  margin:0 !important;
}

/* Also kill any gaps the element container might add around that markdown */
[data-testid="stVerticalBlock"]{
  gap: 0 !important;
}

html{
  /* keeps layout stable and avoids tiny edge seams when scrollbars appear/disappear */
  scrollbar-gutter: stable both-edges;
}
"""

# 4b) Typography baseline
STREAMLIT_CSS_TYPO = """
/* Body baseline (leave brand weight; keep global color as-is) */
body, .stApp{
  font-family:'FrutigerforUBSWeb','FrutigerForUBSWeb','Frutiger','Helvetica Neue',Arial,sans-serif;
  font-weight:300 !important;
  color: var(--ubs-black) !important;   /* keep global; we'll set Streamlit text to black below */
  -webkit-font-smoothing:antialiased; -moz-osx-font-smoothing:grayscale;
}

/* Apply default text styling specifically to Streamlit markdown content */
[data-testid="stMarkdownContainer"]{
  color: var(--ubs-black);                  /* make default text black */
}

/* Default body & list copy (slightly larger) */
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li{
  font-weight:300;
  font-size:17px;                           /* was 16px — slight bump */
  line-height:1.625rem;                     /* keep 26px line-height for the UBS rhythm */
  color: inherit;                            /* inherit black from container */
}
"""

# 4c) st.title / st.header / st.subheader / st.subtitle
# Scope ONLY to Streamlit heading components (doesn't touch custom HTML/markdown).
STREAMLIT_CSS_TITLES = """
/* st.title (H1) — large */
[data-testid="stHeading"] h1,
[data-testid="stMarkdownHeadingContainer"] h1{
  font-family:'FrutigerforUBSWeb','FrutigerForUBSWeb','Frutiger','Helvetica Neue',Arial,sans-serif !important;
  font-weight:400; font-size:56px; line-height:1.1; letter-spacing:.1px; color:var(--ubs-gray-dark);
  margin:0 0 18px 0; position:relative;
}
[data-testid="stHeading"] h1::after,
[data-testid="stMarkdownHeadingContainer"] h1::after{
  content:""; display:block; width:72px; height:4px; margin-top:8px; background:var(--ubs-red);
}

/* st.header (H2) — match 'Our services' */
[data-testid="stHeading"] h2,
[data-testid="stMarkdownHeadingContainer"] h2{
  font-family:'FrutigerforUBSWeb','FrutigerForUBSWeb','Frutiger','Helvetica Neue',Arial,sans-serif !important;
  font-weight:400; font-size:2.5rem; line-height:3rem; letter-spacing:.1px; color:var(--ubs-gray-dark);
  margin:0 0 18px 0; position:relative;
}
[data-testid="stHeading"] h2::after,
[data-testid="stMarkdownHeadingContainer"] h2::after{
  content:""; display:block; width:72px; height:4px; margin-top:8px; background:var(--ubs-red);
}

/* st.subheader + st.subtitle — match 'Discover a clearer financial future' */
[data-testid="stHeading"] h3,
[data-testid="stHeading"] h4,
[data-testid="stMarkdownHeadingContainer"] h3,
[data-testid="stMarkdownHeadingContainer"] h4{
  font-family:'FrutigerforUBSWeb','FrutigerForUBSWeb','Frutiger','Helvetica Neue',Arial,sans-serif !important;
  font-weight:400; font-size:24px; line-height:2.25rem; letter-spacing:.1px; color:var(--ubs-gray-dark);
  margin:0 0 16px 0; position:relative;
}
[data-testid="stHeading"] h3::after,
[data-testid="stHeading"] h4::after,
[data-testid="stMarkdownHeadingContainer"] h3::after,
[data-testid="stMarkdownHeadingContainer"] h4::after{
  content:""; display:block; width:72px; height:4px; margin-top:8px; background:var(--ubs-red);
}
"""

# 4d) st.tabs
STREAMLIT_CSS_TABS = """
[data-testid="stTabs"] [role="tablist"],
[data-testid="stTabs"] [data-baseweb="tab-list"]{
  position: relative;
  border-bottom: 1px solid #e0ded6;
}
[data-testid="stTabs"] [data-baseweb="tab-highlight"]{
  background: var(--ubs-red) !important;
  height: 3px !important;
  border-radius: 0 !important;
  pointer-events: none !important;
  transition: transform 200ms ease, width 200ms ease !important;
  will-change: transform, width;
  z-index: 0;
}
[data-testid="stTabs"] [role="tab"],
[data-testid="stTabs"] [data-baseweb="tab"]{
  font-family:'FrutigerforUBSWeb','Frutiger',Arial,sans-serif;
  font-weight:400; font-size:16px; line-height:1.4;
  color: var(--ubs-gray-dark); background:transparent !important; border:0 !important; box-shadow:none !important;
  margin:0; padding:10px 14px; border-radius:0; cursor:pointer; user-select:none; transition: color 120ms ease;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"],
[data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"]{
  color: var(--ubs-gray-dark) !important;
}
[data-testid="stTabs"] [role="tab"]:hover,
[data-testid="stTabs"] [data-baseweb="tab"]:hover{
  color: var(--ubs-black);
}
"""

# 4e) st.chat_input
STREAMLIT_CSS_CHAT_INPUT = """
[data-testid="stChatInput"]{ max-width:none !important; width:100% !important; margin:0 !important; padding:0 !important; }
[data-testid="stChatInput"] form, [data-testid="stChatInput"] > div{ position:relative !important; }
[data-testid="stChatInput"] textarea{
  width:100% !important; font-family:'FrutigerforUBSWeb','Frutiger',Arial,sans-serif;
  font-size:16px; line-height:1.4; color:var(--ubs-black);
  border:1.5px solid var(--ubs-red); border-radius:999px; background:#fff;
  padding:12px 48px 12px 16px !important; box-shadow:none !important;
}
[data-testid="stChatInput"] textarea:focus{ outline:none !important; box-shadow:none !important; border-color:var(--ubs-red) !important; }
[data-testid="stChatInput"] textarea::placeholder{ color:#6b6f72; opacity:1; }
[data-testid="stChatInput"] :not(textarea):is(:focus, :focus-visible, :focus-within){ outline:none !important; box-shadow:none !important; border:0 !important; border-color:transparent !important; }
[data-testid="stChatInput"] :is([data-baseweb],[data-baseweb="base-input"],[data-baseweb="textarea"],[data-baseweb="form-control-container"],[data-baseweb="input"]){
  border:0 !important; box-shadow:none !important; outline:none !important; background:transparent !important;
}
[data-testid="stChatInput"] :is([data-baseweb],[data-baseweb="base-input"],[data-baseweb="textarea"],[data-baseweb="form-control-container"],[data-baseweb="input"])::before,
[data-testid="stChatInput"] :is([data-baseweb],[data-baseweb="base-input"],[data-baseweb="textarea"],[data-baseweb="form-control-container"],[data-baseweb="input"])::after{
  content:none !important;
}
[data-testid="stChatInput"] textarea:focus-visible{ outline:none !important; box-shadow:none !important; }
[data-testid="stChatInput"] button{
  position:absolute !important; right:6px; top:50%; transform:translateY(-50%);
  width:36px; height:36px; min-width:36px; display:inline-flex; align-items:center; justify-content:center;
  padding:0; margin:0; background:var(--ubs-red) !important; color:#fff !important;
  border:0 !important; border-radius:999px !important; box-shadow:none !important;
}
[data-testid="stChatInput"] button:focus,
[data-testid="stChatInput"] button:active{ box-shadow:none !important; outline:none !important; }
"""

# 4f) st.container helpers (band/rail)
STREAMLIT_CSS_CONTAINERS = """
.st-key-chat_band{ background:var(--ubs-gray-light); padding:32px 0; }
.st-key-chat_band [data-testid*="lement-container"],
.st-key-chat_band [data-testid="stVerticalBlock"]{ padding-left:0 !important; padding-right:0 !important; gap:0 !important; }
.st-key-chat_rail{ max-width:var(--grid-container-width); margin:0 auto; padding:0 var(--grid-container-spacing); box-sizing:content-box; }
.st-key-chat_rail > [data-testid="stVerticalBlock"]{ padding:0 !important; }
.st-key-chat_rail [data-testid*="lement-container"]{ padding-left:0 !important; padding-right:0 !important; }
.st-key-chat_rail [data-testid="stChatInput"],
.st-key-chat_rail [data-testid="stTabs"]{ max-width:none !important; width:100% !important; margin:0 !important; padding:0 !important; }
"""

# 4e.1) st.text_input — dark grey square outline
STREAMLIT_CSS_TEXT_INPUT = """
/* Scope strictly to st.text_input */
[data-testid="stTextInput"] [data-baseweb="input"]{
  border:1.5px solid var(--ubs-gray-dark) !important;
  border-radius:0 !important;
  box-shadow:none !important;
  background:#fff !important;
}

/* Neutralize inner baseweb wrapper so the container border is the only outline */
[data-testid="stTextInput"] [data-baseweb="base-input"]{
  border:0 !important;
  box-shadow:none !important;
  background:transparent !important;
}

/* Input element itself — no extra borders, keep your typography */
[data-testid="stTextInput"] input{
  border:0 !important;
  outline:none !important;
  box-shadow:none !important;
  font-family:'FrutigerforUBSWeb','FrutigerForUBSWeb','Frutiger','Helvetica Neue',Arial,sans-serif;
  font-size:16px; line-height:1.4; color:var(--ubs-black);
}

/* Keep the same border on focus (square + dark grey) */
[data-testid="stTextInput"] [data-baseweb="input"]:focus-within{
  border-color: var(--ubs-gray-dark) !important;
}
"""

# 4e.2) st.popover — dark grey square outline (trigger button only)
STREAMLIT_CSS_POPOVER = """
[data-testid="stPopover"] button{
  border:1.5px solid var(--ubs-gray-dark) !important;
  border-radius:0 !important;
  box-shadow:none !important;
  background:#fff !important;
  color: var(--ubs-black) !important;
}
[data-testid="stPopover"] button:hover,
[data-testid="stPopover"] button:focus,
[data-testid="stPopover"] button:focus-visible{
  border-color: var(--ubs-gray-dark) !important;
  box-shadow:none !important;
}
"""

def inject_streamlit_css() -> None:
    st.markdown(
        "<style>"
        + fontface_blocks()
        + STREAMLIT_CSS_GLOBAL
        + STREAMLIT_CSS_TYPO
        + STREAMLIT_CSS_TITLES
        + STREAMLIT_CSS_TABS
        + STREAMLIT_CSS_CHAT_INPUT
        + STREAMLIT_CSS_CONTAINERS
        + STREAMLIT_CSS_TEXT_INPUT
        + STREAMLIT_CSS_POPOVER
        + "</style>",
        unsafe_allow_html=True,
    )