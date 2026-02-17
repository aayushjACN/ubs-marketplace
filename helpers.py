# helpers.py
"""
General helpers:
- ubs_container(): like st.container, but emits outer/inner wrappers + optional inline CSS
- section_spacer(): small spacer hook between sections (full-bleed)
"""
from __future__ import annotations
from contextlib import contextmanager
from typing import Optional, Dict, Any, List
import base64, mimetypes, os, html
import streamlit as st
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions

load_dotenv()

account_name = os.environ.get("AZURE_STORAGE_ACCOUNT_NAME")
account_key = os.environ.get("AZURE_STORAGE_ACCOUNT_KEY")
container_name = os.environ.get("AZURE_STORAGE_CONTAINER_NAME")

def get_signed_url(blob_name: str) -> str | None:
    if not account_name or not account_key or not container_name:
        st.error("❌ Missing environment variables! Please check your container configuration.")
        return None

    try:
        sas_token = generate_blob_sas(
            account_name=account_name,
            container_name=container_name,
            blob_name=blob_name,
            account_key=account_key,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(hours=1) # Link valid for 1 hour
        )
        return f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"
    except Exception as e:
        st.error(f"Error generating SAS token: {e}")
        return None
    

def _css_inline(style: Optional[Dict[str, str]]) -> str:
    if not style:
        return ""
    return "; ".join(f"{k}:{v}" for k, v in style.items())

def _inject(css: str) -> None:
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

@contextmanager
def ubs_container(
    name: Optional[str] = None,
    *,
    add_default_css: bool = True,
    background: str = "grey",               # "grey" (default) or "white"
    band_style: Optional[Dict[str, str]] = None,
    rail_style: Optional[Dict[str, str]] = None,
):
    """
    Usage:
        with ubs_container():  # default grey band
            ...

        with ubs_container(background="white"):
            ...
    """
    # Stable per-session auto keys
    if "_ubs_seq" not in st.session_state:
        st.session_state["_ubs_seq"] = 0
    st.session_state["_ubs_seq"] += 1
    seq = st.session_state["_ubs_seq"]

    base = name or f"ubs_{seq}"
    band_key = f"{base}_band"
    rail_key = f"{base}_rail"

    # Pick background color (default preserves existing grey)
    bg_choice = (background or "grey").strip().lower()
    band_bg = "var(--ubs-gray-light)" if bg_choice == "grey" else "#ffffff"

    with st.container(key=band_key):
        if add_default_css:
            _inject(
                f"""
.st-key-{band_key}{{ background:{band_bg}; padding:32px 0; }}
.st-key-{band_key} [data-testid*="lement-container"],
.st-key-{band_key} [data-testid="stVerticalBlock"]{{ padding-left:0 !important; padding-right:0 !important; gap:0 !important; }}
"""
            )
        if band_style:
            _inject(f".st-key-{band_key}{{{_css_inline(band_style)}}}")

        with st.container(key=rail_key):
            if add_default_css:
                _inject(
                    f"""
.st-key-{rail_key}{{ max-width:var(--grid-container-width); margin:0 auto; padding:0 var(--grid-container-spacing); box-sizing:content-box; }}
.st-key-{rail_key} > [data-testid="stVerticalBlock"]{{ padding:0 !important; }}
.st-key-{rail_key} [data-testid*="lement-container"]{{ padding-left:0 !important; padding-right:0 !important; }}
.st-key-{rail_key} [data-testid="stChatInput"],
.st-key-{rail_key} [data-testid="stTabs"]{{ max-width:none !important; width:100% !important; margin:0 !important; padding:0 !important; }}
"""
                )
            if rail_style:
                _inject(f".st-key-{rail_key}{{{_css_inline(rail_style)}}}")

            yield

def section_spacer(size: str | None = None) -> None:
    """Full-bleed white band with exact height (no wrapper margins)."""
    style = f"--spacer-size:{size};" if size else ""
    st.markdown(
        f"<div class='full-bleed section-spacer' style='{style}' aria-hidden='true'></div>",
        unsafe_allow_html=True,
    )

# ---------- one-time CSS ----------
def inject_app_card_css_once() -> None:
    #if st.session_state.get("_app_card_css_done"): return
    st.session_state["_app_card_css_done"] = True
    st.markdown("""
<style>
/* ===== Card shell ===== */
.ubs-app-card{
  background:#fff; border:1px solid #dcdcdc; border-radius:0;
  box-sizing:border-box; width:100%;
  display:flex; gap:20px; align-items:flex-start;
  margin-bottom:24px; /* ensure vertical separation between rows */
}

/* Featured (row) — bigger thumb, tiny depth */
.ubs-app-card--row{
  --thumb:220px;               /* was 140px — make the featured image feel substantial */
  box-shadow:0 4px 10px rgba(0,0,0,.04);
  padding:20px;
}
.ubs-app-card--clamp{ max-width:900px; } /* removed when clamp_width=False */

/* ===== Tile cards — fixed height to align rows perfectly ===== */
.ubs-app-card--tile{
  --tile-height: 560px;        /* tune if needed */
  display:flex; flex-direction:column; padding:0;
  height: var(--tile-height);  /* FIX: exact height (not min-height) to keep rows straight */
  box-shadow:none; overflow:hidden;
}

/* ===== Image & status ===== */
.ubs-app-card__thumbwrap{ position:relative; width:var(--thumb); flex:0 0 var(--thumb); }
.ubs-app-card__thumb{
  width:100%; aspect-ratio:4/3; object-fit:cover; object-position:center;
  border:0; background:#f3f3f3;
  filter:grayscale(10%) saturate(.82) contrast(.98);
}
.ubs-app-card__status{
  position:absolute; top:8px; left:8px;
  background:rgba(255,255,255,.92);
  border:1px solid #e5e5e5;
  padding:1px 6px;
  font-size:11px; line-height:14px; font-weight:600; letter-spacing:.02em;
  color:#6b6f72;
}

/* Tile = image on top (about half of card height) — robust against Safari aspect-ratio quirks */
.ubs-app-card--tile .ubs-app-card__thumbwrap{
  width:100%; height: calc(var(--tile-height) * 0.46); /* FIX: explicit height prevents row overlap */
  flex:0 0 auto;
}
.ubs-app-card--tile .ubs-app-card__thumb{
  width:100%; height:100%; object-fit:cover; object-position:center; display:block;
}

/* ===== Content ===== */
.ubs-app-card__body{ flex:1 1 auto; min-width:0; }
.ubs-app-card--row .ubs-app-card__body{ padding:0; }
.ubs-app-card--tile .ubs-app-card__body{ padding:20px 20px 28px 20px; display:flex; flex-direction:column; flex:1 1 auto; }

.ubs-app-card__title{
  font-family:'UBS Headline','UBSHeadline','Walbaum',Georgia,'Times New Roman',serif;
  font-weight:400; font-size:20px; line-height:1.25; letter-spacing:.1px; color:#444; margin:0;
  display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; /* FIX: cap to 2 lines for uniform height */
}
.ubs-app-card--row .ubs-app-card__title{ font-size:24px; color:#222; }

.ubs-app-card__desc{
  font-family:'FrutigerforUBSWeb','FrutigerForUBSWeb','Frutiger','Helvetica Neue',Arial,sans-serif;
  font-size:16px; line-height:1.625rem; color:#111;
  margin:8px 0 10px 0; max-width:60ch;
  display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; /* 2-line clamp */
}

/* Tags (first = business line, second = function) */
.ubs-app-card__tags{ display:flex; flex-wrap:wrap; gap:6px; margin-top:6px; margin-bottom:10px; } /* FIX: adds space below tags */
.ubs-app-card__tag{ border:1px solid #cfcfcf; padding:2px 8px; font-size:12px; line-height:16px; font-weight:500; color:#111; }

/* Actions — one primary + subtle links; pinned bottom on tiles */
.ubs-app-card__actions{
  margin-top:16px; display:flex; flex-wrap:wrap; gap:12px 18px; align-items:center;
}
.ubs-app-card--tile .ubs-app-card__actions{ margin-top:auto; } /* keeps actions at the bottom of fixed-height tiles */

.ubs-btn-primary{
  display:inline-flex; align-items:center; justify-content:center; padding:10px 16px;
  font-weight:700; font-size:14px; text-decoration:none; background:var(--ubs-red,#E60000);
  color:#fff !important; border:0; border-radius:0;
}
.ubs-btn-primary:hover{ filter:brightness(.95); }

.ubs-app-card__actions a{ color:#111 !important; text-decoration:none; font-weight:700; }
.ubs-app-card__actions a:hover{ text-decoration:underline; }

.ubs-chev{ width:16px; height:16px; display:inline-block; stroke:var(--ubs-red,#E60000); fill:none;
  stroke-width:2; stroke-linecap:round; stroke-linejoin:round; }

/* Mobile */
@media (max-width: 640px){
  .ubs-app-card--row{ flex-direction:column; padding:16px; }
  .ubs-app-card__thumbwrap{ width:100%; flex:0 0 auto; }
}
                
/* Ensure the primary button stays white even inside the actions row */
.ubs-app-card__actions .ubs-btn-primary,
.ubs-btn-primary,
.ubs-btn-primary:link,
.ubs-btn-primary:visited{
  color:#fff !important;
}
                
/* ===== Featured (2× width, 1/2 height), image LEFT — same styling as tiles ===== */
.ubs-app-card--feature{
  border:1px solid #dcdcdc; background:#fff; box-shadow:none;
  display:flex; flex-direction:row; align-items:stretch;
  gap:0;
  padding:0 8px 0 0;                 /* tighter right edge */
  height: calc(var(--tile-height) * 0.5);
  overflow:visible;                   /* <— allow stripe to render outside */
  margin-bottom:24px;
  position:relative;                  /* <— anchor for ::before stripe */
}

/* Stripe outside the card; card’s 1px left border now sits against the image */
.ubs-app-card--feature::before{
  content:"";
  position:absolute;
  left: calc(-1px - var(--stripe-width,4px) - var(--stripe-offset,28px));
  top:0;
  bottom:0;                           /* full card/image height */
  width: var(--stripe-width,4px);     /* same thickness as header/hero */
  background: var(--ubs-red,#E60000);
}             

.ubs-app-card--feature .ubs-app-card__thumbwrap{
  flex:1 1 auto; width:auto; height:100%;
  margin-left:0; padding-left:0;      /* <— no gap; border touches image */
  background:transparent;             /* no grey bars */
  position:relative;
  box-sizing:border-box;
}
.ubs-app-card--feature .ubs-app-card__thumb{
  width:100%; height:100%; display:block;
  aspect-ratio:auto;                  /* override global 4/3 */
  object-fit:cover;                   /* match card height; crop sides if needed */
  object-position:center;
  filter:grayscale(10%) saturate(.82) contrast(.98);
}

/* Right content pane — reuse tile measurements */
.ubs-app-card--feature .ubs-app-card__body{
  padding:20px;
  display:flex; flex-direction:column; min-width:0;
  flex: 0 1 calc(1200px);        /* 1.3× wider */
  max-width: calc(1200px);
  margin-right:0;
  margin-left:0;                      /* <— no extra gap; stripe is outside now */
}
                
.ubs-app-card--feature .ubs-app-card__actions{
  white-space:nowrap;                  /* keep on one line */
}

/* Keep tile typography scales for parity */
.ubs-app-card--feature .ubs-app-card__title{
  font-size:20px; line-height:1.25; color:#111; margin:0;
  display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden;
}
.ubs-app-card--feature .ubs-app-card__desc{
  font-size:16px; line-height:1.6; color:#111;
  margin:12px 0 14px 0; max-width:60ch;
  display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden;
}

/* Tags & actions — same rhythm; actions pinned to bottom */
.ubs-app-card--feature .ubs-app-card__tags{
  display:flex; flex-wrap:wrap; gap:6px; margin-top:6px; margin-bottom:12px;
}
.ubs-app-card--feature .ubs-app-card__actions{
  margin-top:auto; padding-top:8px; border-top:1px solid #eee;
  display:flex; flex-wrap:wrap; gap:12px 18px; align-items:center;
}

/* Ensure the red primary keeps white text */
.ubs-app-card--feature .ubs-btn-primary,
.ubs-app-card--feature .ubs-btn-primary:link,
.ubs-app-card--feature .ubs-btn-primary:visited{ color:#fff !important; }

/* Responsive: single-column fallback; match tile height on mobile */
@media (max-width: 960px){
  .ubs-app-card--feature{
    flex-direction:column;
    height: var(--tile-height);
  }
  .ubs-app-card--feature .ubs-app-card__thumbwrap{
    width:100%; flex:0 0 auto; height:calc(var(--tile-height) * 0.46);
  }
}

/* Quiet featured cues */

.ubs-feature-kicker{
  font-family:'FrutigerforUBSWeb','Frutiger','Helvetica Neue',Arial,sans-serif;
  font-size:12px; line-height:1.2;
  text-transform:uppercase; letter-spacing:.04em;
  color:#6b6f72; margin:0 0 6px 0;
}         

/* Make room for the stripe before the text block */
.ubs-app-card--feature .ubs-app-card__body{
  margin-left: calc(var(--stripe-offset) + var(--stripe-width));
}
                                                              
</style>
""", unsafe_allow_html=True)


# ---------- robust image resolver (URL or local file) ----------
@st.cache_data(show_spinner=False)
def _image_to_data_uri(path: str) -> Optional[str]:
    if not path:
        return None
    p = path.strip()
    if p.startswith(("http://", "https://", "data:")):
        return p
    if os.path.exists(p) and os.path.isfile(p):
        mime, _ = mimetypes.guess_type(p)
        mime = mime or "image/png"
        with open(p, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("ascii")
        return f"data:{mime};base64,{b64}"
    return None

# ---------- reusable renderer ----------
def render_app_card(
    app: Dict[str, Any],
    *,
    variant: str = "row",   # "row" (featured) or "tile" (grid)
    clamp_width: bool = True,
    top_margin_px: int = 12
) -> None:
    """
    Renders a reusable application card for an AI App Marketplace.

    Required: title, description
    Optional: image, app_url, demo_url, docs_url, tags, owner, business_line, function, status
    """
    inject_app_card_css_once()

    # --- Content extraction ---
    title = html.escape(app.get("title", "Untitled application"))
    desc  = html.escape(app.get("description", ""))
    img   = _image_to_data_uri(app.get("image", "")) or ""
    alt   = html.escape(app.get("alt", title))

    app_url  = (app.get("app_url")  or "").strip()
    demo_url = (app.get("demo_url") or "").strip()
    docs_url = (app.get("docs_url") or "").strip()

    if demo_url:
        azure_demo_url = get_signed_url(demo_url)
        if azure_demo_url:
            demo_url = azure_demo_url
        else:
            st.warning(f"⚠️ Could not generate signed URL for demo: {demo_url}")
     
    # Tags: enforce business line + function as the only tags shown on the card
    business_line = (app.get("business_line") or "").strip()
    function      = (app.get("function") or "").strip()

    tags_tokens: List[str] = []
    if business_line: tags_tokens.append(business_line)
    if function:      tags_tokens.append(function)

    tags_html = ""
    if tags_tokens:
        tags_html = "<div class='ubs-app-card__tags'>" + "".join(
            f"<span class='ubs-app-card__tag'>{html.escape(t)}</span>" for t in tags_tokens
        ) + "</div>"

    # Status: only show muted "Preview"; map "Beta" -> "Preview"; anything else -> hide
    status_raw = (app.get("status") or "").strip().lower()
    status = "Preview" if status_raw in ("beta", "preview") else ""
    status_html = f"<span class='ubs-app-card__status'>{status}</span>" if status else ""

    # One primary (Open app), two subtle links (Watch demo, Read docs)
    chev = """<svg class="ubs-chev" viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M5 3l5 5-5 5"></path></svg>"""

    actions: List[str] = []
    if app_url:
        # primary button always present when we have an app_url
        actions.append(f"<a href='{html.escape(app_url)}' target='_blank' rel='noopener noreferrer' class='ubs-btn-primary'>Open app</a>")
    if demo_url:
      actions.append(f"<a  href='{html.escape(demo_url)}' >Watch demo {chev}</a>")
    if docs_url:
      actions.append(f"<a  href='{html.escape(docs_url)}' target='_blank' rel='noopener noreferrer'>Read docs {chev}</a>")

    actions_html = f"<div class='ubs-app-card__actions'>{''.join(actions)}</div>" if actions else ""

    # Classes
    variant_class = {"row":"ubs-app-card--row",
                     "tile":"ubs-app-card--tile",
                     "feature": "ubs-app-card--feature"
                     }.get(variant,"ubs-app-card--tile")
    clamp_class   = "ubs-app-card--clamp" if clamp_width and variant=="row" else ""

    # Layout:
    # - row: side-by-side thumb + body (keeps your featured design)
    # - tile: image on top (full width), body below; CSS pins actions to bottom
    is_feature_compact = (variant == "feature")
    kicker_html = "<div class='ubs-feature-kicker'>Featured application</div>" if is_feature_compact else ""
    if is_feature_compact:
        card_html = f"""
    <div class="ubs-app-card {variant_class} {clamp_class}" style="margin-top:{int(top_margin_px)}px">
      <div class="ubs-app-card__thumbwrap">
        <img src="{img}" alt="{alt}" class="ubs-app-card__thumb"/>
        {status_html}
      </div>
      <div class="ubs-app-card__body">
        {kicker_html}
        <h3 class="ubs-app-card__title">{title}</h3>
        <p class="ubs-app-card__desc">{desc}</p>
        {tags_html}
        {actions_html}
      </div>
    </div>
    """
    else:
        card_html = f"""
<div class="ubs-app-card {variant_class} {clamp_class}" style="margin-top:{int(top_margin_px)}px">
  <div class="ubs-app-card__thumbwrap">
    <img src="{img}" alt="{alt}" class="ubs-app-card__thumb"/>
    {status_html}
  </div>
  <div class="ubs-app-card__body">
    <h3 class="ubs-app-card__title">{title}</h3>
    <p class="ubs-app-card__desc">{desc}</p>
    {tags_html}
    {actions_html}
  </div>
</div>
"""
    st.markdown(card_html, unsafe_allow_html=True)