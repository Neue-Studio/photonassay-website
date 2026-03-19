#!/usr/bin/env python3
"""
Build script for Chrysos PhotonAssay inner pages.
Reads the logo SVG from index.html, generates 8 HTML pages with shared
design system, nav (with dropdowns), footer, sticky CTA, and scroll-reveal JS.
"""

import re
import os

SITE_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Extract logo SVG from homepage ──────────────────────────────────────────

def extract_logo_svg():
    with open(os.path.join(SITE_DIR, 'index.html'), 'r') as f:
        content = f.read()
    match = re.search(r'(<svg class="nav__logo-svg".*?</svg>)', content, re.DOTALL)
    if not match:
        raise RuntimeError("Could not extract logo SVG from index.html")
    return match.group(1)

LOGO_SVG = extract_logo_svg()

# ── Shared HTML shell ───────────────────────────────────────────────────────

def page_shell(title, body_content, active_link=None):
    """Generate a full HTML page with shared head, nav, footer, sticky CTA, JS."""

    # Determine which nav link is active
    def nav_active(link_name):
        return ' nav__link--active' if active_link == link_name else ''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — PhotonAssay™ by Chrysos Corporation</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@200;300;400;500&display=swap" rel="stylesheet">
  <style>
    /* ============================================
       DESIGN SYSTEM
       ============================================ */
    :root {{
      --black: #000000;
      --near-black: #0A0A0A;
      --dark: #111111;
      --charcoal: #1A1A1A;
      --grey-900: #222222;
      --grey-700: #555555;
      --grey-500: #888888;
      --grey-300: #BBBBBB;
      --grey-100: #E8E8E8;
      --white: #FFFFFF;
      --offwhite: #FAFAFA;
      --gold: #F2B705;
      --gold-hover: #D9A404;
      --font: 'Roboto', -apple-system, BlinkMacSystemFont, sans-serif;
      --space-1: 8px; --space-2: 16px; --space-3: 24px; --space-4: 32px;
      --space-5: 40px; --space-6: 48px; --space-8: 64px; --space-10: 80px;
      --space-12: 96px; --space-15: 120px; --space-20: 160px;
      --max-width: 1320px; --nav-height: 80px; --section-pad: 160px; --container-pad: 48px;
    }}

    /* RESET */
    *, *::before, *::after {{ margin: 0; padding: 0; box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }}
    body {{
      font-family: var(--font);
      font-weight: 300;
      font-size: 17px;
      line-height: 1.75;
      color: var(--grey-500);
      background: var(--white);
      overflow-x: hidden;
    }}
    img {{ max-width: 100%; display: block; }}
    a {{ text-decoration: none; color: inherit; }}
    button {{ font-family: inherit; cursor: pointer; border: none; background: none; }}

    /* TYPOGRAPHY */
    h1 {{
      font-weight: 300;
      font-size: 88px;
      line-height: 1.04;
      letter-spacing: -0.04em;
      color: var(--white);
    }}
    h2 {{
      font-weight: 200;
      font-size: 56px;
      line-height: 1.1;
      letter-spacing: -0.03em;
      color: var(--black);
    }}
    h3 {{
      font-weight: 400;
      font-size: 24px;
      line-height: 1.3;
      letter-spacing: -0.015em;
      color: var(--black);
    }}
    h4 {{
      font-weight: 500;
      font-size: 18px;
      line-height: 1.4;
      letter-spacing: -0.01em;
      color: var(--black);
    }}
    .eyebrow {{
      font-size: 11px;
      font-weight: 500;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      color: var(--grey-500);
      margin-bottom: var(--space-4);
      display: flex;
      align-items: center;
      gap: 16px;
    }}
    .eyebrow::before {{
      content: '';
      display: block;
      width: 60px;
      height: 2px;
      background: var(--gold);
    }}

    /* LAYOUT */
    .container {{
      max-width: var(--max-width);
      margin: 0 auto;
      padding: 0 var(--container-pad);
    }}

    /* SCROLL REVEAL */
    .reveal {{
      opacity: 0;
      transform: translateY(48px);
      transition: opacity 0.8s ease, transform 0.8s ease;
    }}
    .reveal.is-visible {{
      opacity: 1;
      transform: translateY(0);
    }}

    /* ============================================
       BUTTONS
       ============================================ */
    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 10px;
      padding: 16px 40px;
      font-family: var(--font);
      font-size: 12px;
      font-weight: 500;
      letter-spacing: 0.16em;
      text-transform: uppercase;
      border: 1px solid var(--black);
      background: transparent;
      color: var(--black);
      cursor: pointer;
      transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
      text-decoration: none;
    }}
    .btn:hover {{
      background: var(--black);
      color: var(--white);
      box-shadow: inset 0 -3px 0 var(--gold);
    }}
    .btn--light {{
      border-color: var(--white);
      color: var(--white);
    }}
    .btn--light:hover {{
      background: var(--white);
      color: var(--black);
      box-shadow: inset 0 -3px 0 var(--gold);
    }}
    .btn--gold {{
      border: none;
      background: var(--gold);
      color: var(--near-black);
    }}
    .btn--gold:hover {{
      background: var(--gold-hover);
      box-shadow: 0 4px 20px rgba(242, 183, 5, 0.3);
    }}
    .arrow-link {{
      font-size: 13px;
      font-weight: 500;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--grey-500);
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: color 0.3s ease;
    }}
    .arrow-link:hover {{
      color: var(--gold);
    }}
    .arrow-link svg {{
      transition: transform 0.3s ease;
    }}
    .arrow-link:hover svg {{
      transform: translateX(4px);
    }}

    /* ============================================
       NAVIGATION
       ============================================ */
    .nav {{
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      z-index: 1000;
      height: var(--nav-height);
      display: flex;
      align-items: center;
      background: transparent;
      transition: background 0.5s ease, backdrop-filter 0.5s ease;
    }}
    .nav--scrolled {{
      background: rgba(0, 0, 0, 0.95);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
    }}
    .nav--dark {{
      background: rgba(0, 0, 0, 0.95);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
    }}
    .nav__inner {{
      max-width: var(--max-width);
      width: 100%;
      margin: 0 auto;
      padding: 0 var(--container-pad);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .nav__logo {{
      display: flex;
      align-items: baseline;
      gap: 8px;
    }}
    .nav__logo-svg {{
      height: 43px;
      width: auto;
      color: var(--white);
      display: block;
    }}
    .nav__links {{
      display: flex;
      align-items: center;
      gap: var(--space-5);
    }}
    .nav__link {{
      font-size: 12px;
      font-weight: 400;
      letter-spacing: 0.16em;
      text-transform: uppercase;
      color: var(--grey-300);
      position: relative;
      padding-bottom: 2px;
      transition: color 0.3s ease;
    }}
    .nav__link::after {{
      content: '';
      position: absolute;
      bottom: 0;
      left: 0;
      width: 100%;
      height: 2px;
      background: var(--gold);
      transform: scaleX(0);
      transform-origin: left;
      transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    .nav__link:hover {{
      color: var(--white);
    }}
    .nav__link:hover::after {{
      transform: scaleX(1);
    }}
    .nav__link--active {{
      color: var(--white);
    }}
    .nav__link--active::after {{
      transform: scaleX(1);
    }}

    /* NAV DROPDOWNS */
    .nav__dropdown {{
      position: relative;
    }}
    .nav__dropdown-menu {{
      position: absolute;
      top: 100%;
      left: 0;
      min-width: 220px;
      background: var(--near-black);
      border: 1px solid rgba(255,255,255,0.08);
      padding: 8px 0;
      opacity: 0;
      visibility: hidden;
      transform: translateY(8px);
      transition: all 0.25s ease;
      z-index: 1000;
    }}
    .nav__dropdown:hover .nav__dropdown-menu {{
      opacity: 1;
      visibility: visible;
      transform: translateY(0);
    }}
    .nav__dropdown-menu a {{
      display: block;
      padding: 10px 20px;
      color: var(--grey-300);
      font-size: 13px;
      font-weight: 400;
      letter-spacing: 0.02em;
      text-decoration: none;
      transition: color 0.2s, background 0.2s;
      text-transform: none;
    }}
    .nav__dropdown-menu a:hover {{
      color: var(--white);
      background: rgba(255,255,255,0.04);
    }}

    /* ============================================
       STICKY CTA TAB
       ============================================ */
    .sticky-cta {{
      position: fixed;
      right: 0;
      top: 50%;
      transform: translateY(-50%);
      z-index: 999;
      writing-mode: vertical-rl;
      text-orientation: mixed;
    }}
    .sticky-cta__link {{
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 16px 10px;
      background: var(--gold);
      color: var(--near-black);
      font-size: 12px;
      font-weight: 600;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      text-decoration: none;
      border-radius: 8px 0 0 8px;
      transition: padding 0.3s ease, background 0.3s ease;
    }}
    .sticky-cta__link:hover {{
      padding-right: 16px;
      background: #f5c842;
    }}
    .sticky-cta__link svg {{
      width: 14px;
      height: 14px;
      transform: rotate(-90deg);
    }}

    /* ============================================
       PAGE HERO (inner pages — not full viewport)
       ============================================ */
    .page-hero {{
      background: var(--near-black);
      padding: calc(var(--nav-height) + var(--space-15)) 0 var(--space-15);
    }}
    .page-hero h1 {{
      font-size: 64px;
      margin-bottom: var(--space-3);
    }}
    .page-hero__subtitle {{
      font-size: 19px;
      font-weight: 300;
      color: var(--grey-300);
      max-width: 560px;
      line-height: 1.7;
    }}

    /* ============================================
       SECTIONS
       ============================================ */
    .section-light {{
      background: var(--white);
      padding: var(--section-pad) 0;
    }}
    .section-offwhite {{
      background: var(--offwhite);
      padding: var(--section-pad) 0;
    }}
    .section-dark {{
      background: var(--near-black);
      padding: var(--section-pad) 0;
    }}
    .section-dark h2 {{ color: var(--white); }}
    .section-dark h3 {{ color: var(--white); }}
    .section-dark .eyebrow {{ color: var(--grey-300); }}
    .section-black {{
      background: var(--black);
      padding: var(--section-pad) 0;
    }}
    .section-black h2 {{ color: var(--white); }}
    .section-black h3 {{ color: var(--white); }}
    .section-black .eyebrow {{ color: var(--grey-300); }}

    /* ============================================
       CARDS
       ============================================ */
    .card {{
      border: 1px solid var(--grey-100);
      border-radius: 2px;
      overflow: hidden;
      transition: border-color 0.3s ease, transform 0.3s ease;
    }}
    .card:hover {{
      border-color: var(--grey-300);
      transform: translateY(-4px);
    }}
    .card__image {{
      width: 100%;
      aspect-ratio: 16/9;
      background: var(--grey-100);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 13px;
      font-weight: 400;
      color: var(--grey-500);
      letter-spacing: 0.02em;
    }}
    .card__body {{
      padding: var(--space-4);
    }}
    .card__type {{
      font-size: 11px;
      font-weight: 500;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      color: var(--gold);
      margin-bottom: var(--space-1);
    }}
    .card__title {{
      font-size: 20px;
      font-weight: 400;
      color: var(--black);
      letter-spacing: -0.015em;
      line-height: 1.3;
      margin-bottom: var(--space-2);
    }}
    .card__excerpt {{
      font-size: 15px;
      color: var(--grey-500);
      line-height: 1.65;
      margin-bottom: var(--space-3);
    }}
    .card__date {{
      font-size: 13px;
      color: var(--grey-500);
    }}

    /* Dark card variant */
    .card--dark {{
      border-color: rgba(255,255,255,0.06);
      background: rgba(255,255,255,0.02);
    }}
    .card--dark:hover {{
      border-color: rgba(242, 183, 5, 0.2);
    }}
    .card--dark .card__title {{ color: var(--white); }}
    .card--dark .card__excerpt {{ color: var(--grey-300); }}

    /* ============================================
       3-COL GRID
       ============================================ */
    .grid-3 {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: var(--space-4);
    }}
    .grid-2 {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: var(--space-4);
    }}

    /* ============================================
       PLACEHOLDER IMAGE
       ============================================ */
    .placeholder-img {{
      background: var(--grey-100);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 13px;
      font-weight: 400;
      color: var(--grey-500);
      letter-spacing: 0.02em;
      border-radius: 2px;
    }}

    /* ============================================
       TYPE BADGE
       ============================================ */
    .badge {{
      display: inline-block;
      font-size: 10px;
      font-weight: 500;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      padding: 4px 12px;
      border-radius: 2px;
      background: rgba(242, 183, 5, 0.1);
      color: var(--gold);
    }}
    .badge--outline {{
      background: transparent;
      border: 1px solid var(--grey-100);
      color: var(--grey-500);
    }}

    /* ============================================
       STAT BLOCK
       ============================================ */
    .stat {{
      text-align: center;
    }}
    .stat__number {{
      font-size: 72px;
      font-weight: 200;
      letter-spacing: -0.03em;
      line-height: 1;
      color: var(--gold);
      margin-bottom: var(--space-1);
    }}
    .stat__label {{
      font-size: 13px;
      font-weight: 500;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--grey-500);
    }}

    /* ============================================
       QUOTE BLOCK
       ============================================ */
    .quote-block {{
      border-left: 3px solid var(--gold);
      padding-left: var(--space-4);
    }}
    .quote-block__text {{
      font-size: 24px;
      font-weight: 300;
      line-height: 1.5;
      letter-spacing: -0.01em;
      color: var(--white);
      margin-bottom: var(--space-3);
    }}
    .quote-block__author {{
      font-size: 14px;
      font-weight: 500;
      color: var(--grey-300);
    }}
    .quote-block__role {{
      font-size: 13px;
      color: var(--grey-500);
    }}

    /* ============================================
       BREADCRUMB
       ============================================ */
    .breadcrumb {{
      padding: calc(var(--nav-height) + var(--space-4)) 0 var(--space-2);
      background: var(--offwhite);
    }}
    .breadcrumb__list {{
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 13px;
      color: var(--grey-500);
      list-style: none;
    }}
    .breadcrumb__list a {{
      color: var(--grey-500);
      transition: color 0.3s;
    }}
    .breadcrumb__list a:hover {{
      color: var(--gold);
    }}
    .breadcrumb__sep {{
      color: var(--grey-300);
    }}

    /* ============================================
       FORM STYLES (shared)
       ============================================ */
    .form__group {{
      display: flex;
      flex-direction: column;
      margin-bottom: var(--space-3);
    }}
    .form__label {{
      font-size: 13px;
      font-weight: 500;
      color: var(--black);
      letter-spacing: 0.02em;
      margin-bottom: var(--space-1);
    }}
    .form__label .required {{
      color: var(--gold);
      margin-left: 2px;
    }}
    .form__input,
    .form__select,
    .form__textarea {{
      font-family: var(--font);
      font-size: 15px;
      font-weight: 300;
      color: var(--black);
      background: var(--white);
      border: 1px solid var(--grey-100);
      padding: 14px 16px;
      border-radius: 2px;
      transition: border-color 0.3s ease, box-shadow 0.3s ease;
      outline: none;
      -webkit-appearance: none;
      appearance: none;
    }}
    .form__input:focus,
    .form__select:focus,
    .form__textarea:focus {{
      border-color: var(--gold);
      box-shadow: 0 0 0 3px rgba(242, 183, 5, 0.08);
    }}
    .form__input::placeholder,
    .form__textarea::placeholder {{
      color: var(--grey-300);
      font-weight: 300;
    }}
    .form__textarea {{
      resize: vertical;
      min-height: 120px;
      line-height: 1.6;
    }}
    .form__row {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: var(--space-3);
      margin-bottom: var(--space-3);
    }}
    .form__row .form__group {{
      margin-bottom: 0;
    }}

    /* ============================================
       RESOURCE TABLE
       ============================================ */
    .resource-table {{
      width: 100%;
      border-collapse: collapse;
    }}
    .resource-table__row {{
      display: grid;
      grid-template-columns: 1fr 140px 2fr 60px;
      gap: var(--space-3);
      align-items: center;
      padding: var(--space-3) 0;
      border-bottom: 1px solid var(--grey-100);
      transition: background 0.2s;
    }}
    .resource-table__row:hover {{
      background: var(--offwhite);
    }}
    .resource-table__title {{
      font-size: 16px;
      font-weight: 400;
      color: var(--black);
    }}
    .resource-table__desc {{
      font-size: 14px;
      color: var(--grey-500);
    }}
    .resource-table__arrow {{
      color: var(--grey-300);
      transition: color 0.3s, transform 0.3s;
      display: flex;
      justify-content: flex-end;
    }}
    .resource-table__row:hover .resource-table__arrow {{
      color: var(--gold);
      transform: translateX(4px);
    }}

    /* TABS */
    .tabs {{
      display: flex;
      gap: var(--space-1);
      margin-bottom: var(--space-6);
      border-bottom: 1px solid var(--grey-100);
    }}
    .tab {{
      padding: var(--space-2) var(--space-3);
      font-size: 13px;
      font-weight: 500;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: var(--grey-500);
      border-bottom: 2px solid transparent;
      cursor: pointer;
      transition: color 0.3s, border-color 0.3s;
    }}
    .tab:hover {{ color: var(--black); }}
    .tab--active {{
      color: var(--black);
      border-bottom-color: var(--gold);
    }}

    /* SEARCH */
    .search-bar {{
      position: relative;
      margin-bottom: var(--space-5);
    }}
    .search-bar__input {{
      width: 100%;
      font-family: var(--font);
      font-size: 15px;
      font-weight: 300;
      color: var(--black);
      background: var(--offwhite);
      border: 1px solid var(--grey-100);
      padding: 16px 20px 16px 48px;
      border-radius: 2px;
      outline: none;
      transition: border-color 0.3s;
    }}
    .search-bar__input:focus {{
      border-color: var(--gold);
    }}
    .search-bar__icon {{
      position: absolute;
      left: 16px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--grey-300);
    }}

    /* ============================================
       ARTICLE
       ============================================ */
    .article {{
      max-width: 720px;
      margin: 0 auto;
    }}
    .article__meta {{
      display: flex;
      align-items: center;
      gap: var(--space-2);
      margin-bottom: var(--space-4);
    }}
    .article__date {{
      font-size: 14px;
      color: var(--grey-500);
    }}
    .article h1 {{
      color: var(--black);
      font-size: 48px;
      font-weight: 200;
      line-height: 1.15;
      letter-spacing: -0.03em;
      margin-bottom: var(--space-4);
    }}
    .article__author {{
      font-size: 14px;
      color: var(--grey-500);
      margin-bottom: var(--space-8);
    }}
    .article__body p {{
      margin-bottom: var(--space-4);
    }}
    .article__body h2 {{
      font-size: 32px;
      margin-top: var(--space-8);
      margin-bottom: var(--space-3);
    }}
    .article__pullquote {{
      border-left: 3px solid var(--gold);
      padding-left: var(--space-4);
      margin: var(--space-6) 0;
      font-size: 22px;
      font-weight: 300;
      color: var(--black);
      line-height: 1.5;
      letter-spacing: -0.01em;
    }}

    /* SHARE LINKS */
    .share {{
      display: flex;
      align-items: center;
      gap: var(--space-2);
      margin-top: var(--space-8);
      padding-top: var(--space-4);
      border-top: 1px solid var(--grey-100);
    }}
    .share__label {{
      font-size: 12px;
      font-weight: 500;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--grey-500);
    }}
    .share__icon {{
      width: 36px;
      height: 36px;
      border: 1px solid var(--grey-100);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--grey-500);
      transition: color 0.3s, border-color 0.3s;
    }}
    .share__icon:hover {{
      color: var(--gold);
      border-color: var(--gold);
    }}

    /* ============================================
       TIMELINE
       ============================================ */
    .timeline {{
      position: relative;
      padding-left: var(--space-6);
    }}
    .timeline::before {{
      content: '';
      position: absolute;
      left: 0;
      top: 0;
      bottom: 0;
      width: 2px;
      background: var(--grey-100);
    }}
    .timeline__item {{
      position: relative;
      padding-bottom: var(--space-8);
    }}
    .timeline__item:last-child {{
      padding-bottom: 0;
    }}
    .timeline__dot {{
      position: absolute;
      left: calc(-1 * var(--space-6) - 5px);
      top: 4px;
      width: 12px;
      height: 12px;
      border-radius: 50%;
      background: var(--gold);
    }}
    .timeline__year {{
      font-size: 14px;
      font-weight: 500;
      letter-spacing: 0.1em;
      color: var(--gold);
      text-transform: uppercase;
      margin-bottom: var(--space-1);
    }}
    .timeline__title {{
      font-size: 20px;
      font-weight: 400;
      color: var(--black);
      margin-bottom: var(--space-1);
    }}
    .timeline__desc {{
      font-size: 15px;
      color: var(--grey-500);
      line-height: 1.65;
    }}

    /* ============================================
       CTA BAND
       ============================================ */
    .cta-band {{
      text-align: center;
      padding: var(--space-12) 0;
    }}
    .cta-band h2 {{
      max-width: 640px;
      margin: 0 auto var(--space-5);
    }}

    /* ============================================
       NEWSLETTER
       ============================================ */
    .newsletter {{
      max-width: 480px;
      margin: 0 auto;
      text-align: center;
    }}
    .newsletter__form {{
      display: flex;
      gap: var(--space-2);
      margin-top: var(--space-4);
    }}
    .newsletter__form input {{
      flex: 1;
      font-family: var(--font);
      font-size: 15px;
      font-weight: 300;
      padding: 14px 20px;
      border: 1px solid rgba(255,255,255,0.15);
      background: rgba(255,255,255,0.05);
      color: var(--white);
      border-radius: 2px;
      outline: none;
      transition: border-color 0.3s;
    }}
    .newsletter__form input:focus {{
      border-color: var(--gold);
    }}
    .newsletter__form input::placeholder {{
      color: var(--grey-500);
    }}

    /* EVENT FORM */
    .event-form {{
      background: var(--offwhite);
      border: 1px solid var(--grey-100);
      border-radius: 2px;
      padding: var(--space-6);
      max-width: 560px;
    }}

    /* ============================================
       FOOTER
       ============================================ */
    .footer {{
      background: var(--black);
      padding: var(--space-10) 0;
    }}
    .footer__inner {{
      display: flex;
      justify-content: space-between;
      align-items: start;
      padding-bottom: var(--space-8);
      border-bottom: 1px solid rgba(255,255,255,0.08);
      margin-bottom: var(--space-5);
    }}
    .footer__brand {{
      max-width: 360px;
    }}
    .footer__logo {{
      font-size: 14px;
      font-weight: 500;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--white);
      margin-bottom: var(--space-2);
    }}
    .footer__tagline {{
      font-size: 15px;
      font-weight: 300;
      color: var(--grey-500);
      line-height: 1.6;
    }}
    .footer__links {{
      display: flex;
      gap: var(--space-8);
    }}
    .footer__col-title {{
      font-size: 11px;
      font-weight: 500;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      color: var(--grey-500);
      margin-bottom: var(--space-3);
    }}
    .footer__col a {{
      display: block;
      font-size: 14px;
      font-weight: 300;
      color: var(--grey-300);
      margin-bottom: var(--space-2);
      transition: color 0.3s ease;
    }}
    .footer__col a:hover {{
      color: var(--gold);
    }}
    .footer__bottom {{
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .footer__copyright {{
      font-size: 13px;
      color: var(--grey-500);
    }}
    .footer__legal {{
      display: flex;
      gap: var(--space-4);
    }}
    .footer__legal a {{
      font-size: 13px;
      color: var(--grey-500);
      transition: color 0.3s ease;
    }}
    .footer__legal a:hover {{
      color: var(--grey-300);
    }}

    /* ============================================
       RESPONSIVE
       ============================================ */
    @media (max-width: 768px) {{
      :root {{
        --section-pad: 80px;
        --container-pad: 24px;
      }}
      h1 {{ font-size: 40px; }}
      h2 {{ font-size: 32px; }}
      .nav__links {{ display: none; }}
      .page-hero h1 {{ font-size: 36px; }}
      .grid-3 {{ grid-template-columns: 1fr; }}
      .grid-2 {{ grid-template-columns: 1fr; }}
      .resource-table__row {{
        grid-template-columns: 1fr;
        gap: var(--space-1);
      }}
      .resource-table__desc {{ display: none; }}
      .stat__number {{ font-size: 48px; }}
      .article h1 {{ font-size: 32px; }}
      .newsletter__form {{ flex-direction: column; }}
      .form__row {{ grid-template-columns: 1fr; }}
      .footer__inner {{
        flex-direction: column;
        gap: var(--space-6);
      }}
      .footer__bottom {{
        flex-direction: column;
        gap: var(--space-3);
        text-align: center;
      }}
      .footer__legal {{
        flex-wrap: wrap;
        justify-content: center;
      }}
      .sticky-cta {{ display: none; }}
    }}

    /* PAGE-SPECIFIC OVERRIDES ARE INJECTED BELOW */
  </style>
</head>
<body>

  <!-- NAVIGATION -->
  <nav class="nav nav--dark" id="nav">
    <div class="nav__inner">
      <a href="index.html" class="nav__logo">
        {LOGO_SVG}
      </a>
      <div class="nav__links">
        <div class="nav__dropdown">
          <a href="resources.html" class="nav__link{nav_active('resources')}">Resources</a>
          <div class="nav__dropdown-menu">
            <a href="resource-example.html">Technical Note Example</a>
            <a href="case-study-example.html">Case Study Example</a>
          </div>
        </div>
        <div class="nav__dropdown">
          <a href="latest.html" class="nav__link{nav_active('latest')}">Latest</a>
          <div class="nav__dropdown-menu">
            <a href="news-example.html">News Article Example</a>
            <a href="event-example.html">Event Example</a>
          </div>
        </div>
        <a href="about.html" class="nav__link{nav_active('about')}">About Us</a>
        <a href="contact.html" class="nav__link{nav_active('contact')}">Contact</a>
      </div>
    </div>
  </nav>

  {body_content}

  <!-- FOOTER -->
  <footer class="footer">
    <div class="container">
      <div class="footer__inner">
        <div class="footer__brand">
          <div class="footer__logo">Chrysos Corporation</div>
          <p class="footer__tagline">Chrysos Corporation Ltd is the company behind PhotonAssay&#8482;, a breakthrough technology for rapid, non-destructive elemental analysis of geological samples.</p>
        </div>
        <div class="footer__links">
          <div class="footer__col">
            <div class="footer__col-title">Company</div>
            <a href="about.html">About Us</a>
            <a href="https://chrysoscorp.com/careers" target="_blank">Careers</a>
            <a href="contact.html">Contact</a>
          </div>
          <div class="footer__col">
            <div class="footer__col-title">Resources</div>
            <a href="resources.html">Case Studies</a>
            <a href="resources.html">Technical Papers</a>
            <a href="latest.html">News</a>
          </div>
        </div>
      </div>
      <div class="footer__bottom">
        <div class="footer__copyright">&copy; 2026 Chrysos Corporation Ltd. All rights reserved.</div>
        <div class="footer__legal">
          <a href="#">Privacy Policy</a>
          <a href="#">Terms of Use</a>
        </div>
      </div>
    </div>
  </footer>

  <!-- STICKY CTA -->
  <div class="sticky-cta">
    <a href="contact.html" class="sticky-cta__link">
      Get In Touch
      <svg viewBox="0 0 12 12" fill="none"><path d="M3 9L9 3M9 3H4M9 3V8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
    </a>
  </div>

  <!-- SCROLL REVEAL JS -->
  <script>
    const nav = document.getElementById('nav');
    window.addEventListener('scroll', () => {{
      if (window.scrollY > 100) {{
        nav.classList.add('nav--scrolled');
      }} else {{
        nav.classList.remove('nav--scrolled');
      }}
    }}, {{ passive: true }});

    const revealObserver = new IntersectionObserver((entries) => {{
      entries.forEach(entry => {{
        if (entry.isIntersecting) {{
          entry.target.classList.add('is-visible');
          revealObserver.unobserve(entry.target);
        }}
      }});
    }}, {{
      threshold: 0.12,
      rootMargin: '0px 0px -40px 0px'
    }});
    document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));
  </script>

</body>
</html>'''


# ── ARROW SVG ───────────────────────────────────────────────────────────────

ARROW_SVG = '<svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M1 7H13M13 7L7 1M13 7L7 13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ARROW_DIAG_SVG = '<svg width="12" height="12" viewBox="0 0 12 12" fill="none"><path d="M1 11L11 1M11 1H3M11 1v8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
SEARCH_SVG = '<svg width="18" height="18" viewBox="0 0 18 18" fill="none"><circle cx="7.5" cy="7.5" r="5.5" stroke="currentColor" stroke-width="1.5"/><path d="M12 12L16 16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>'

# ── PAGE: resources.html ────────────────────────────────────────────────────

def build_resources():
    body = f'''
  <!-- PAGE HERO -->
  <section class="page-hero">
    <div class="container">
      <p class="eyebrow">Resources</p>
      <h1>Technical library</h1>
      <p class="page-hero__subtitle">Access technical notes, performance data, webinar recordings, and case studies to understand what PhotonAssay&#8482; can deliver for your operation.</p>
    </div>
  </section>

  <!-- HIGHLIGHTED CONTENT -->
  <section class="section-light">
    <div class="container">
      <div class="reveal">
        <p class="eyebrow">Featured Resources</p>
        <h2 style="margin-bottom: var(--space-8);">Start here</h2>
      </div>
      <div class="grid-3 reveal">
        <div class="card">
          <div class="card__image">Case Study Image &mdash; 16:9</div>
          <div class="card__body">
            <div class="card__type">Case Study</div>
            <div class="card__title">Ravenswood Gold Mine: On-site PhotonAssay deployment</div>
            <p class="card__excerpt">How a tier-one Queensland gold operation reduced assay turnaround from 48 hours to under 2 minutes.</p>
            <a href="ravenswood.html" class="arrow-link">Read case study {ARROW_SVG}</a>
          </div>
        </div>
        <div class="card">
          <div class="card__image">Webinar Thumbnail &mdash; 16:9</div>
          <div class="card__body">
            <div class="card__type">Webinar</div>
            <div class="card__title">PhotonAssay&#8482; for Gold: Measurement Performance Deep Dive</div>
            <p class="card__excerpt">A 45-minute walkthrough of gold measurement accuracy, repeatability, and real-world performance data.</p>
            <a href="#" class="arrow-link">Watch recording {ARROW_SVG}</a>
          </div>
        </div>
        <div class="card">
          <div class="card__image">Technical Document &mdash; 16:9</div>
          <div class="card__body">
            <div class="card__type">Technical Note</div>
            <div class="card__title">TN-101: Measurement Performance for Gold Ore Samples</div>
            <p class="card__excerpt">The definitive reference on PhotonAssay&#8482; accuracy, precision, and performance benchmarks against fire assay.</p>
            <a href="resource-example.html" class="arrow-link">View resource {ARROW_SVG}</a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- CTA BAND -->
  <section class="section-dark cta-band">
    <div class="container reveal">
      <h2 style="color: var(--white); font-size: 40px;">Navigating information around a new technology can be challenging. Let us help you.</h2>
      <a href="contact.html" class="btn btn--light" style="margin-top: var(--space-4);">Get In Touch {ARROW_SVG}</a>
    </div>
  </section>

  <!-- RESOURCE DOWNLOAD MATRIX -->
  <section class="section-light">
    <div class="container">
      <div class="reveal">
        <p class="eyebrow">All Resources</p>
        <h2 style="margin-bottom: var(--space-6);">Browse our library</h2>
      </div>

      <div class="reveal">
        <div class="search-bar">
          <span class="search-bar__icon">{SEARCH_SVG}</span>
          <input type="text" class="search-bar__input" placeholder="Search resources by title or keyword...">
        </div>
      </div>

      <div class="reveal">
        <div class="tabs">
          <div class="tab tab--active">All</div>
          <div class="tab">Technical Notes</div>
          <div class="tab">Performance Notes</div>
          <div class="tab">Webinars</div>
          <div class="tab">Case Studies</div>
        </div>
      </div>

      <div class="reveal">
        <div class="resource-table__row">
          <div class="resource-table__title">TN-101: Measurement Performance for Gold Ore Samples</div>
          <div><span class="badge">Technical Note</span></div>
          <div class="resource-table__desc">Gold assay accuracy, precision, and repeatability benchmarks across diverse ore types.</div>
          <div class="resource-table__arrow">{ARROW_DIAG_SVG}</div>
        </div>
        <div class="resource-table__row">
          <div class="resource-table__title">TN-102: Sample Preparation Guidelines</div>
          <div><span class="badge">Technical Note</span></div>
          <div class="resource-table__desc">Best practices for sample preparation to maximise PhotonAssay&#8482; measurement quality.</div>
          <div class="resource-table__arrow">{ARROW_DIAG_SVG}</div>
        </div>
        <div class="resource-table__row">
          <div class="resource-table__title">TN-103: Multi-Element Analysis Capabilities</div>
          <div><span class="badge">Technical Note</span></div>
          <div class="resource-table__desc">Overview of additional elements measurable by PhotonAssay, including silver and copper.</div>
          <div class="resource-table__arrow">{ARROW_DIAG_SVG}</div>
        </div>
        <div class="resource-table__row">
          <div class="resource-table__title">PN-201: Fire Assay Comparison &mdash; Gold in Oxide Ores</div>
          <div><span class="badge badge--outline">Performance Note</span></div>
          <div class="resource-table__desc">Head-to-head comparison of PhotonAssay and fire assay on oxide ore samples from Western Australia.</div>
          <div class="resource-table__arrow">{ARROW_DIAG_SVG}</div>
        </div>
        <div class="resource-table__row">
          <div class="resource-table__title">PN-202: Repeatability &amp; Reproducibility Study</div>
          <div><span class="badge badge--outline">Performance Note</span></div>
          <div class="resource-table__desc">Statistical analysis of measurement consistency across multiple PhotonAssay units.</div>
          <div class="resource-table__arrow">{ARROW_DIAG_SVG}</div>
        </div>
        <div class="resource-table__row">
          <div class="resource-table__title">Webinar: Gold Measurement Performance Deep Dive</div>
          <div><span class="badge">Webinar</span></div>
          <div class="resource-table__desc">45-minute technical walkthrough covering accuracy, precision, and real-world lab performance data.</div>
          <div class="resource-table__arrow">{ARROW_DIAG_SVG}</div>
        </div>
        <div class="resource-table__row">
          <div class="resource-table__title">Webinar: Operating Models for PhotonAssay Deployment</div>
          <div><span class="badge">Webinar</span></div>
          <div class="resource-table__desc">Understanding the three deployment models — commercial lab, mine-site lease, and direct purchase.</div>
          <div class="resource-table__arrow">{ARROW_DIAG_SVG}</div>
        </div>
        <div class="resource-table__row">
          <div class="resource-table__title">Case Study: Ravenswood Gold Mine</div>
          <div><span class="badge">Case Study</span></div>
          <div class="resource-table__desc">On-site deployment delivering 2-minute turnaround and improved grade control at a Queensland gold mine.</div>
          <div class="resource-table__arrow">{ARROW_DIAG_SVG}</div>
        </div>
        <div class="resource-table__row">
          <div class="resource-table__title">Case Study: SGS Minerals &mdash; Commercial Lab Adoption</div>
          <div><span class="badge">Case Study</span></div>
          <div class="resource-table__desc">How a major global laboratory integrated PhotonAssay into its commercial workflow.</div>
          <div class="resource-table__arrow">{ARROW_DIAG_SVG}</div>
        </div>
        <div class="resource-table__row">
          <div class="resource-table__title">TN-104: Environmental &amp; Safety Benefits</div>
          <div><span class="badge">Technical Note</span></div>
          <div class="resource-table__desc">Eliminating lead, eliminating scope 1 emissions, and improving laboratory safety outcomes.</div>
          <div class="resource-table__arrow">{ARROW_DIAG_SVG}</div>
        </div>
      </div>
    </div>
  </section>

  <!-- NEWSLETTER CTA -->
  <section class="section-dark">
    <div class="container reveal">
      <div class="newsletter">
        <p class="eyebrow" style="justify-content: center;">Stay Informed</p>
        <h2 style="color: var(--white); font-size: 36px;">Get the latest from PhotonAssay&#8482;</h2>
        <p style="color: var(--grey-300); margin-top: var(--space-2);">Technical updates, deployment news, and industry insights delivered to your inbox.</p>
        <div class="newsletter__form">
          <input type="email" placeholder="Your email address">
          <a href="#" class="btn btn--gold">Subscribe</a>
        </div>
      </div>
    </div>
  </section>
'''
    return page_shell("Resources", body, active_link="resources")


# ── PAGE: resource-example.html ─────────────────────────────────────────────

def build_resource_example():
    body = f'''
  <!-- BREADCRUMB -->
  <div class="breadcrumb">
    <div class="container">
      <ul class="breadcrumb__list">
        <li><a href="resources.html">Resources</a></li>
        <li class="breadcrumb__sep">/</li>
        <li><a href="resources.html">Technical Notes</a></li>
        <li class="breadcrumb__sep">/</li>
        <li>TN-101</li>
      </ul>
    </div>
  </div>

  <!-- RESOURCE HEADER -->
  <section class="section-offwhite" style="padding-top: var(--space-6);">
    <div class="container">
      <div class="article reveal">
        <span class="badge" style="margin-bottom: var(--space-3);">Technical Note</span>
        <h1>PhotonAssay&#8482; Measurement Performance for Gold Ore Samples</h1>
        <div class="article__meta">
          <span class="article__date">TN-101 &middot; Updated March 2026</span>
        </div>
        <p style="font-size: 18px; color: var(--grey-700); line-height: 1.7; margin-bottom: var(--space-6);">This technical note presents comprehensive measurement performance data for PhotonAssay&#8482; across a range of gold ore types. It covers accuracy, precision, repeatability, and direct comparisons with traditional fire assay methods.</p>
      </div>
    </div>
  </section>

  <!-- DOWNLOAD SECTION -->
  <section class="section-light">
    <div class="container">
      <div class="article reveal">
        <div style="background: var(--offwhite); border: 1px solid var(--grey-100); border-radius: 2px; padding: var(--space-6); text-align: center;">
          <div class="placeholder-img" style="width: 100%; height: 200px; margin-bottom: var(--space-4);">Document Preview &mdash; First Page</div>
          <h3 style="margin-bottom: var(--space-2);">Download the full technical note</h3>
          <p style="font-size: 15px; color: var(--grey-500); margin-bottom: var(--space-4);">PDF &middot; 12 pages &middot; 2.4 MB</p>
          <a href="#" class="btn btn--gold">Download PDF {ARROW_DIAG_SVG}</a>
          <p style="font-size: 13px; color: var(--grey-500); margin-top: var(--space-3);">This download is gated via HubSpot. You may be asked to provide your email address.</p>
        </div>

        <div style="margin-top: var(--space-10);">
          <h2 style="font-size: 32px; margin-bottom: var(--space-4);">What this note covers</h2>
          <ul style="list-style: none; padding: 0;">
            <li style="padding: var(--space-2) 0; border-bottom: 1px solid var(--grey-100); color: var(--grey-700);">Gold measurement accuracy across oxide, sulphide, and transitional ore types</li>
            <li style="padding: var(--space-2) 0; border-bottom: 1px solid var(--grey-100); color: var(--grey-700);">Precision and repeatability at low, medium, and high gold grades</li>
            <li style="padding: var(--space-2) 0; border-bottom: 1px solid var(--grey-100); color: var(--grey-700);">Direct comparison with 50g fire assay on matched sample pairs</li>
            <li style="padding: var(--space-2) 0; border-bottom: 1px solid var(--grey-100); color: var(--grey-700);">Statistical methodology and reporting standards</li>
            <li style="padding: var(--space-2) 0; color: var(--grey-700);">Implications for grade control and resource estimation</li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <!-- RELATED RESOURCES -->
  <section class="section-offwhite">
    <div class="container">
      <div class="reveal">
        <p class="eyebrow">Related Resources</p>
        <h2 style="margin-bottom: var(--space-8); font-size: 40px;">You might also find useful</h2>
      </div>
      <div class="grid-3 reveal">
        <div class="card">
          <div class="card__image">Document Preview &mdash; 16:9</div>
          <div class="card__body">
            <div class="card__type">Technical Note</div>
            <div class="card__title">TN-102: Sample Preparation Guidelines</div>
            <p class="card__excerpt">Best practices for sample preparation to maximise measurement quality.</p>
            <a href="#" class="arrow-link">View resource {ARROW_SVG}</a>
          </div>
        </div>
        <div class="card">
          <div class="card__image">Document Preview &mdash; 16:9</div>
          <div class="card__body">
            <div class="card__type">Performance Note</div>
            <div class="card__title">PN-201: Fire Assay Comparison &mdash; Gold in Oxide Ores</div>
            <p class="card__excerpt">Head-to-head comparison across oxide ore samples from Western Australia.</p>
            <a href="#" class="arrow-link">View resource {ARROW_SVG}</a>
          </div>
        </div>
        <div class="card">
          <div class="card__image">Webinar Thumbnail &mdash; 16:9</div>
          <div class="card__body">
            <div class="card__type">Webinar</div>
            <div class="card__title">Gold Measurement Performance Deep Dive</div>
            <p class="card__excerpt">45-minute walkthrough of accuracy, precision, and real-world performance data.</p>
            <a href="#" class="arrow-link">Watch recording {ARROW_SVG}</a>
          </div>
        </div>
      </div>
    </div>
  </section>
'''
    return page_shell("TN-101: Measurement Performance for Gold Ore Samples", body, active_link="resources")


# ── PAGE: case-study-example.html ───────────────────────────────────────────

def build_case_study_example():
    return build_case_study(
        title="Case Study Template",
        page_title="Ravenswood Gold Mine",
        client_name="Ravenswood Gold Mine",
        location="Queensland, Australia",
        hero_stat="97%",
        hero_stat_label="faster turnaround",
        intro="When a tier-one Queensland gold operation needed to eliminate assay bottlenecks and improve grade control, they deployed PhotonAssay&#8482; directly on site. The results transformed their entire workflow.",
        challenge="Ravenswood Gold Mine relied on traditional fire assay for all gold analysis, with samples transported to an off-site commercial laboratory. Turnaround times of 24 to 48 hours created delays in grade control decisions, impacting blast planning and ore routing. Sample transport added cost and introduced chain-of-custody complexity. Inconsistent fire assay results across different laboratories meant reconciliation was an ongoing challenge.",
        solution="Chrysos worked with Ravenswood to deploy a PhotonAssay&#8482; unit directly at the mine site under Operating Model 3 (direct deployment). The unit was installed in a purpose-built facility adjacent to the sample preparation area, enabling geologists to receive results within minutes of sample submission. Training for on-site operators was completed within two weeks, and the system was fully integrated into the existing grade control workflow.",
        results=[
            ("~2 min", "Analysis time per sample"),
            ("97%", "Faster than fire assay"),
            ("Zero", "Scope 1 emissions from assay"),
            ("500g", "Sample size (vs. 50g fire assay)")
        ],
        quote_text="PhotonAssay has fundamentally changed how we make grade control decisions. We went from waiting days to having actionable data in minutes.",
        quote_author="Chief Geologist",
        quote_role="Ravenswood Gold Mine",
        is_template=True
    )


# ── PAGE: ravenswood.html (populated case study) ────────────────────────────

def build_ravenswood():
    return build_case_study(
        title="Ravenswood Gold Mine Case Study",
        page_title="Ravenswood Gold Mine",
        client_name="Ravenswood Gold Mine",
        location="Queensland, Australia",
        hero_stat="97%",
        hero_stat_label="faster turnaround",
        intro="When one of Queensland's most significant gold operations needed to eliminate assay bottlenecks and improve real-time grade control, they became one of the first mine sites in Australia to deploy PhotonAssay&#8482; directly on location.",
        challenge="Ravenswood Gold Mine is a large-scale open-pit and underground gold operation in northern Queensland, producing over 200,000 ounces annually. The operation relied entirely on traditional fire assay, with samples couriered to a commercial laboratory in Townsville. Typical turnaround times ranged from 24 to 48 hours, and occasionally stretched longer during peak periods. This delay created a fundamental disconnect between drilling and decision-making. Grade control geologists were making blast and routing decisions based on data that was already a day or more old. Sample transport added logistical complexity, and the site experienced periodic inconsistencies when comparing results across different commercial lab facilities.",
        solution="Chrysos partnered with Ravenswood to deploy a PhotonAssay&#8482; XR unit directly at the mine site under Operating Model 3 &mdash; the direct-to-site deployment model. A purpose-built analysis facility was constructed adjacent to the existing sample preparation area, connected directly into the mine's digital infrastructure. The PhotonAssay unit was configured for high-throughput gold analysis on 500g samples, with results returned in approximately two minutes per sample. On-site geological and laboratory staff completed operator training within two weeks, and the system was fully operational for production use within 30 days of installation. Integration with the mine's geological database allowed real-time results to flow directly into grade control models and block planning tools.",
        results=[
            ("~2 min", "Analysis time per sample"),
            ("97%", "Faster than fire assay"),
            ("Zero", "Scope 1 emissions from assay"),
            ("500g", "Larger sample size analysed"),
            ("24/7", "On-site availability"),
            ("30 days", "Installation to production")
        ],
        quote_text="The speed of PhotonAssay results has changed how we operate. Grade control decisions that used to wait 48 hours are now made the same shift. That kind of responsiveness has a direct impact on our recovery.",
        quote_author="Chief Geologist",
        quote_role="Ravenswood Gold Mine, Queensland",
        is_template=False
    )


def build_case_study(title, page_title, client_name, location, hero_stat, hero_stat_label, intro, challenge, solution, results, quote_text, quote_author, quote_role, is_template=False):
    results_html = ""
    for val, label in results:
        results_html += f'''
        <div class="stat">
          <div class="stat__number">{val}</div>
          <div class="stat__label">{label}</div>
        </div>'''

    body = f'''
  <!-- CASE STUDY HERO -->
  <section class="page-hero" style="padding-bottom: var(--space-10);">
    <div class="container">
      <p class="eyebrow" style="color: var(--grey-300);">Case Study</p>
      <h1 style="margin-bottom: var(--space-2);">{page_title}</h1>
      <p style="font-size: 15px; color: var(--grey-500); margin-bottom: var(--space-5);">{location}</p>
      <div style="display: flex; align-items: baseline; gap: var(--space-2); margin-bottom: var(--space-5);">
        <span style="font-size: 72px; font-weight: 200; color: var(--gold); letter-spacing: -0.03em; line-height: 1;">{hero_stat}</span>
        <span style="font-size: 18px; font-weight: 300; color: var(--grey-300);">{hero_stat_label}</span>
      </div>
      <p class="page-hero__subtitle" style="max-width: 640px;">{intro}</p>
    </div>
  </section>

  <!-- HERO IMAGE -->
  <section class="section-light" style="padding: var(--space-8) 0;">
    <div class="container reveal">
      <div class="placeholder-img" style="width: 100%; height: 420px;">Case Study Hero Image &mdash; Mine Site / PhotonAssay Unit &mdash; 21:9</div>
    </div>
  </section>

  <!-- CHALLENGE -->
  <section class="section-light" style="padding-top: var(--space-10);">
    <div class="container">
      <div style="display: grid; grid-template-columns: 280px 1fr; gap: var(--space-15); align-items: start;" class="reveal">
        <div>
          <p class="eyebrow">The Challenge</p>
        </div>
        <div>
          <p style="font-size: 18px; color: var(--grey-700); line-height: 1.7;">{challenge}</p>
        </div>
      </div>
    </div>
  </section>

  <!-- SOLUTION -->
  <section class="section-light">
    <div class="container">
      <div style="display: grid; grid-template-columns: 280px 1fr; gap: var(--space-15); align-items: start;" class="reveal">
        <div>
          <p class="eyebrow">The Solution</p>
        </div>
        <div>
          <p style="font-size: 18px; color: var(--grey-700); line-height: 1.7;">{solution}</p>
        </div>
      </div>
    </div>
  </section>

  <!-- KEY METRICS -->
  <section class="section-offwhite">
    <div class="container">
      <div class="reveal" style="text-align: center; margin-bottom: var(--space-8);">
        <p class="eyebrow" style="justify-content: center;">Results</p>
        <h2 style="font-size: 40px;">Key outcomes</h2>
      </div>
      <div class="grid-3 reveal" style="gap: var(--space-8);">
        {results_html}
      </div>
    </div>
  </section>

  <!-- QUOTE -->
  <section class="section-dark" style="padding: var(--space-12) 0;">
    <div class="container reveal">
      <div class="quote-block" style="max-width: 720px; margin: 0 auto;">
        <p class="quote-block__text">&ldquo;{quote_text}&rdquo;</p>
        <p class="quote-block__author">{quote_author}</p>
        <p class="quote-block__role">{quote_role}</p>
      </div>
    </div>
  </section>

  <!-- RELATED CASE STUDIES -->
  <section class="section-light">
    <div class="container">
      <div class="reveal">
        <p class="eyebrow">More Case Studies</p>
        <h2 style="margin-bottom: var(--space-8); font-size: 40px;">See how others are using PhotonAssay&#8482;</h2>
      </div>
      <div class="grid-3 reveal">
        <div class="card">
          <div class="card__image">Case Study Image &mdash; 16:9</div>
          <div class="card__body">
            <div class="card__type">Case Study</div>
            <div class="card__title">SGS Minerals: Commercial Lab Adoption</div>
            <p class="card__excerpt">How a major global laboratory integrated PhotonAssay into its commercial workflow.</p>
            <a href="#" class="arrow-link">Read case study {ARROW_SVG}</a>
          </div>
        </div>
        <div class="card">
          <div class="card__image">Case Study Image &mdash; 16:9</div>
          <div class="card__body">
            <div class="card__type">Case Study</div>
            <div class="card__title">Intertek Minerals: Multi-Element Analysis</div>
            <p class="card__excerpt">Expanding beyond gold to deliver silver and copper analysis at commercial scale.</p>
            <a href="#" class="arrow-link">Read case study {ARROW_SVG}</a>
          </div>
        </div>
        <div class="card">
          <div class="card__image">Case Study Image &mdash; 16:9</div>
          <div class="card__body">
            <div class="card__type">Case Study</div>
            <div class="card__title">West African Gold: Remote Deployment</div>
            <p class="card__excerpt">Deploying PhotonAssay in a remote West African mining operation with limited infrastructure.</p>
            <a href="#" class="arrow-link">Read case study {ARROW_SVG}</a>
          </div>
        </div>
      </div>
    </div>
  </section>
'''
    return page_shell(title, body, active_link="resources")


# ── PAGE: latest.html ───────────────────────────────────────────────────────

def build_latest():
    body = f'''
  <!-- PAGE HERO -->
  <section class="page-hero">
    <div class="container">
      <p class="eyebrow">Latest</p>
      <h1>News &amp; Events</h1>
      <p class="page-hero__subtitle">Deployment updates, company news, and upcoming events from Chrysos Corporation and the PhotonAssay&#8482; ecosystem.</p>
    </div>
  </section>

  <!-- FEATURED ARTICLES -->
  <section class="section-light">
    <div class="container">
      <div class="reveal">
        <p class="eyebrow">Featured</p>
        <h2 style="margin-bottom: var(--space-8);">Latest stories</h2>
      </div>
      <div class="grid-3 reveal">
        <div class="card">
          <div class="card__image">News Image &mdash; 16:9</div>
          <div class="card__body">
            <div class="card__type">Deployment</div>
            <div class="card__title">PhotonAssay&#8482; unit begins operations at Ravenswood Gold Mine</div>
            <p class="card__excerpt">A new on-site deployment in Queensland is delivering 2-minute gold analysis and transforming grade control workflows.</p>
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <span class="card__date">12 March 2026</span>
              <a href="news-example.html" class="arrow-link">Read more {ARROW_SVG}</a>
            </div>
          </div>
        </div>
        <div class="card">
          <div class="card__image">News Image &mdash; 16:9</div>
          <div class="card__body">
            <div class="card__type">Product</div>
            <div class="card__title">PhotonAssay&#8482; XN expansion model announced</div>
            <p class="card__excerpt">The next generation of PhotonAssay hardware delivers higher throughput and expanded multi-element capabilities.</p>
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <span class="card__date">4 March 2026</span>
              <a href="#" class="arrow-link">Read more {ARROW_SVG}</a>
            </div>
          </div>
        </div>
        <div class="card">
          <div class="card__image">News Image &mdash; 16:9</div>
          <div class="card__body">
            <div class="card__type">Corporate</div>
            <div class="card__title">Chrysos reports record half-year results</div>
            <p class="card__excerpt">Strong revenue growth driven by new deployments and increasing sample throughput across existing sites.</p>
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <span class="card__date">24 February 2026</span>
              <a href="#" class="arrow-link">Read more {ARROW_SVG}</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- ARCHIVE -->
  <section class="section-offwhite">
    <div class="container">
      <div class="reveal">
        <p class="eyebrow">Archive</p>
        <h2 style="margin-bottom: var(--space-6); font-size: 40px;">Older stories</h2>
      </div>
      <div class="reveal">
        <div class="resource-table__row">
          <div class="resource-table__title">New deployment at Tropicana Gold Mine begins operations</div>
          <div><span class="badge badge--outline">Deployment</span></div>
          <div class="resource-table__desc">PhotonAssay goes live at one of Western Australia's largest gold operations.</div>
          <div class="resource-table__arrow">{ARROW_SVG}</div>
        </div>
        <div class="resource-table__row">
          <div class="resource-table__title">Chrysos signs multi-unit agreement with major lab network</div>
          <div><span class="badge badge--outline">Corporate</span></div>
          <div class="resource-table__desc">A new commercial partnership will see PhotonAssay deployed across five laboratory locations.</div>
          <div class="resource-table__arrow">{ARROW_SVG}</div>
        </div>
        <div class="resource-table__row">
          <div class="resource-table__title">PhotonAssay featured at IMARC 2025</div>
          <div><span class="badge badge--outline">Event</span></div>
          <div class="resource-table__desc">Chrysos presented the latest performance data and deployment case studies at Australia's premier mining conference.</div>
          <div class="resource-table__arrow">{ARROW_SVG}</div>
        </div>
        <div class="resource-table__row">
          <div class="resource-table__title">Silver analysis capability validated in independent study</div>
          <div><span class="badge badge--outline">Product</span></div>
          <div class="resource-table__desc">Third-party testing confirms PhotonAssay silver measurement performance meets commercial laboratory standards.</div>
          <div class="resource-table__arrow">{ARROW_SVG}</div>
        </div>
        <div class="resource-table__row">
          <div class="resource-table__title">Chrysos appoints new Chief Technology Officer</div>
          <div><span class="badge badge--outline">Corporate</span></div>
          <div class="resource-table__desc">Dr. Sarah Mitchell joins from CSIRO to lead the next phase of PhotonAssay product development.</div>
          <div class="resource-table__arrow">{ARROW_SVG}</div>
        </div>
      </div>
    </div>
  </section>

  <!-- UPCOMING EVENTS -->
  <section class="section-light">
    <div class="container">
      <div class="reveal">
        <p class="eyebrow">Events</p>
        <h2 style="margin-bottom: var(--space-6); font-size: 40px;">Upcoming events</h2>
      </div>
      <div class="grid-2 reveal">
        <div class="card">
          <div class="card__body">
            <div class="card__type">Webinar</div>
            <div class="card__title">JORC/NI 43-101 Compliance Webinar</div>
            <p class="card__excerpt">Understanding how PhotonAssay data integrates with international reporting standards for mineral resources.</p>
            <p class="card__date" style="margin-bottom: var(--space-3);">15 April 2026 &middot; 2:00 PM AEST &middot; Online</p>
            <a href="event-example.html" class="arrow-link">Register now {ARROW_SVG}</a>
          </div>
        </div>
        <div class="card">
          <div class="card__body" style="display: flex; align-items: center; justify-content: center; min-height: 200px;">
            <p style="color: var(--grey-500); font-size: 15px;">More events coming soon. <a href="contact.html" style="color: var(--gold);">Get in touch</a> to be notified.</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- NEWSLETTER CTA -->
  <section class="section-dark">
    <div class="container reveal">
      <div class="newsletter">
        <p class="eyebrow" style="justify-content: center; color: var(--grey-300);">Stay Informed</p>
        <h2 style="color: var(--white); font-size: 36px;">Don't miss an update</h2>
        <p style="color: var(--grey-300); margin-top: var(--space-2);">Subscribe to receive deployment news, technical updates, and event invitations.</p>
        <div class="newsletter__form">
          <input type="email" placeholder="Your email address">
          <a href="#" class="btn btn--gold">Subscribe</a>
        </div>
      </div>
    </div>
  </section>
'''
    return page_shell("News & Events", body, active_link="latest")


# ── PAGE: event-example.html ────────────────────────────────────────────────

def build_event_example():
    body = f'''
  <!-- EVENT HERO -->
  <section class="page-hero">
    <div class="container">
      <p class="eyebrow" style="color: var(--grey-300);">Event</p>
      <h1 style="font-size: 48px; max-width: 720px;">JORC/NI 43-101 Compliance Webinar</h1>
      <div style="display: flex; flex-wrap: wrap; gap: var(--space-5); margin-top: var(--space-5);">
        <div>
          <div style="font-size: 11px; font-weight: 500; letter-spacing: 0.14em; text-transform: uppercase; color: var(--gold); margin-bottom: 4px;">Date</div>
          <div style="font-size: 17px; color: var(--grey-300);">15 April 2026</div>
        </div>
        <div>
          <div style="font-size: 11px; font-weight: 500; letter-spacing: 0.14em; text-transform: uppercase; color: var(--gold); margin-bottom: 4px;">Time</div>
          <div style="font-size: 17px; color: var(--grey-300);">2:00 PM &ndash; 3:00 PM AEST</div>
        </div>
        <div>
          <div style="font-size: 11px; font-weight: 500; letter-spacing: 0.14em; text-transform: uppercase; color: var(--gold); margin-bottom: 4px;">Location</div>
          <div style="font-size: 17px; color: var(--grey-300);">Online (Zoom)</div>
        </div>
      </div>
    </div>
  </section>

  <!-- EVENT DETAILS -->
  <section class="section-light">
    <div class="container">
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-15); align-items: start;">
        <div class="reveal">
          <h2 style="font-size: 36px; margin-bottom: var(--space-4);">Understanding Assay Data Quality</h2>
          <p style="margin-bottom: var(--space-4);">As PhotonAssay&#8482; adoption grows, the question of how its data integrates with international mineral resource reporting standards becomes increasingly important. This webinar addresses that directly.</p>
          <p style="margin-bottom: var(--space-4);">Our panel of technical experts will walk through how PhotonAssay results meet the requirements of both JORC Code (2012) and NI 43-101 reporting frameworks. We'll cover data quality assurance protocols, certified reference material performance, and how major audit firms are treating PhotonAssay data in their reviews.</p>
          <h3 style="margin-top: var(--space-6); margin-bottom: var(--space-3);">Who should attend</h3>
          <ul style="list-style: none; padding: 0;">
            <li style="padding: 8px 0; border-bottom: 1px solid var(--grey-100); color: var(--grey-700);">Competent Persons and Qualified Persons preparing mineral resource estimates</li>
            <li style="padding: 8px 0; border-bottom: 1px solid var(--grey-100); color: var(--grey-700);">Laboratory managers overseeing QA/QC programs</li>
            <li style="padding: 8px 0; border-bottom: 1px solid var(--grey-100); color: var(--grey-700);">Mine geologists evaluating alternative assay methods</li>
            <li style="padding: 8px 0; color: var(--grey-700);">Technical advisors and auditors reviewing assay data quality</li>
          </ul>
        </div>

        <div class="reveal">
          <div class="event-form">
            <h3 style="margin-bottom: var(--space-4);">Register for this event</h3>
            <div class="form__row">
              <div class="form__group">
                <label class="form__label">First Name <span class="required">*</span></label>
                <input type="text" class="form__input" placeholder="First name">
              </div>
              <div class="form__group">
                <label class="form__label">Last Name <span class="required">*</span></label>
                <input type="text" class="form__input" placeholder="Last name">
              </div>
            </div>
            <div class="form__group">
              <label class="form__label">Email <span class="required">*</span></label>
              <input type="email" class="form__input" placeholder="your@email.com">
            </div>
            <div class="form__group">
              <label class="form__label">Company</label>
              <input type="text" class="form__input" placeholder="Company name">
            </div>
            <div class="form__group">
              <label class="form__label">Role</label>
              <input type="text" class="form__input" placeholder="Your role or title">
            </div>
            <button class="btn btn--gold" style="width: 100%; justify-content: center; margin-top: var(--space-2);">Register {ARROW_SVG}</button>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- BACK TO LATEST -->
  <section class="section-offwhite" style="padding: var(--space-8) 0;">
    <div class="container">
      <a href="latest.html" class="arrow-link" style="gap: 10px;">
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none" style="transform: rotate(180deg);"><path d="M1 7H13M13 7L7 1M13 7L7 13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
        Back to News &amp; Events
      </a>
    </div>
  </section>
'''
    return page_shell("JORC/NI 43-101 Compliance Webinar", body, active_link="latest")


# ── PAGE: news-example.html ─────────────────────────────────────────────────

def build_news_example():
    body = f'''
  <!-- ARTICLE HEADER -->
  <section class="section-offwhite" style="padding-top: calc(var(--nav-height) + var(--space-10)); padding-bottom: var(--space-10);">
    <div class="container">
      <div class="article reveal">
        <div class="article__meta">
          <span class="badge badge--outline">Deployment</span>
          <span class="article__date">12 March 2026</span>
        </div>
        <h1>PhotonAssay&#8482; unit begins operations at Ravenswood Gold Mine</h1>
        <p class="article__author">Chrysos Corporation</p>
      </div>
    </div>
  </section>

  <!-- ARTICLE IMAGE -->
  <section class="section-light" style="padding: var(--space-6) 0;">
    <div class="container">
      <div class="article reveal">
        <div class="placeholder-img" style="width: 100%; height: 380px; margin-bottom: var(--space-2);">Article Hero Image &mdash; Mine Site / Installation &mdash; 16:9</div>
        <p style="font-size: 13px; color: var(--grey-500); font-style: italic;">The PhotonAssay unit installed at Ravenswood Gold Mine, Queensland.</p>
      </div>
    </div>
  </section>

  <!-- ARTICLE BODY -->
  <section class="section-light" style="padding-top: var(--space-6);">
    <div class="container">
      <div class="article reveal">
        <div class="article__body">
          <p>Chrysos Corporation has announced that a PhotonAssay&#8482; unit has commenced operations at Ravenswood Gold Mine in northern Queensland, Australia. The deployment marks a significant milestone for the technology's adoption in on-site mining environments.</p>

          <p>The unit, installed under Chrysos's Operating Model 3 (direct mine-site deployment), is now delivering gold assay results in approximately two minutes per sample &mdash; a significant reduction from the 24 to 48 hour turnaround times previously experienced with traditional fire assay methods.</p>

          <div class="article__pullquote">The deployment at Ravenswood demonstrates that mine sites can eliminate assay bottlenecks entirely by bringing the analysis to the ore, rather than sending the ore to the analysis.</div>

          <p>Ravenswood Gold Mine is a large-scale open-pit and underground operation producing over 200,000 ounces of gold annually. The mine's geological team had identified assay turnaround as a key constraint on grade control efficiency, particularly during high-throughput drilling campaigns where timely data is critical for blast planning and ore routing.</p>

          <p>The PhotonAssay unit analyses 500-gram samples using high-energy X-ray photons, providing a non-destructive measurement that eliminates the need for lead-based fluxes and high-temperature furnaces used in traditional fire assay. This results in zero scope 1 emissions from the assay process itself, while also removing several occupational health hazards associated with fire assay laboratory operations.</p>

          <h2>Implications for the industry</h2>

          <p>The Ravenswood deployment is one of a growing number of mine-site installations globally. Chrysos now has PhotonAssay units operating across multiple continents, in both commercial laboratory and direct mine-site configurations. The company reports increasing demand for its Operating Model 3 offering as mine operators seek to bring analytical capability closer to the point of decision.</p>
        </div>

        <!-- SHARE -->
        <div class="share">
          <span class="share__label">Share</span>
          <a href="#" class="share__icon">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M8.5 1.5v8M4 5l4.5-4.5L13 5M1.5 10v3a1.5 1.5 0 001.5 1.5h10a1.5 1.5 0 001.5-1.5v-3" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </a>
          <a href="#" class="share__icon">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M13.6 0H9.5l.7 2H12l-3.3 3.3 1.4 1.4L13.6 3.3V5.5l2 .7V0h-2zM0 2.4v11.2C0 14.9 1.1 16 2.4 16h11.2c1.3 0 2.4-1.1 2.4-2.4V8l-2 .7v4.9c0 .2-.2.4-.4.4H2.4c-.2 0-.4-.2-.4-.4V2.4c0-.2.2-.4.4-.4h4.9L8 0H2.4C1.1 0 0 1.1 0 2.4z"/></svg>
          </a>
          <a href="#" class="share__icon">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M2 4l6 4 6-4" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/><rect x="1" y="3" width="14" height="10" rx="1.5" stroke="currentColor" stroke-width="1.2"/></svg>
          </a>
        </div>
      </div>
    </div>
  </section>

  <!-- RELATED NEWS -->
  <section class="section-offwhite">
    <div class="container">
      <div class="reveal">
        <p class="eyebrow">Related News</p>
        <h2 style="margin-bottom: var(--space-8); font-size: 40px;">More stories</h2>
      </div>
      <div class="grid-3 reveal">
        <div class="card">
          <div class="card__image">News Image &mdash; 16:9</div>
          <div class="card__body">
            <div class="card__type">Product</div>
            <div class="card__title">PhotonAssay&#8482; XN expansion model announced</div>
            <p class="card__excerpt">The next generation delivers higher throughput and expanded multi-element capabilities.</p>
            <span class="card__date">4 March 2026</span>
          </div>
        </div>
        <div class="card">
          <div class="card__image">News Image &mdash; 16:9</div>
          <div class="card__body">
            <div class="card__type">Corporate</div>
            <div class="card__title">Chrysos reports record half-year results</div>
            <p class="card__excerpt">Strong revenue growth driven by new deployments and sample throughput increases.</p>
            <span class="card__date">24 February 2026</span>
          </div>
        </div>
        <div class="card">
          <div class="card__image">News Image &mdash; 16:9</div>
          <div class="card__body">
            <div class="card__type">Deployment</div>
            <div class="card__title">Tropicana Gold Mine deployment goes live</div>
            <p class="card__excerpt">Another major Western Australian operation adopts on-site PhotonAssay analysis.</p>
            <span class="card__date">10 February 2026</span>
          </div>
        </div>
      </div>
    </div>
  </section>
'''
    return page_shell("PhotonAssay Unit Begins Operations at Ravenswood", body, active_link="latest")


# ── PAGE: about.html ────────────────────────────────────────────────────────

def build_about():
    body = f'''
  <!-- PAGE HERO -->
  <section class="page-hero">
    <div class="container">
      <p class="eyebrow" style="color: var(--grey-300);">About</p>
      <h1>The future of mineral analysis</h1>
      <p class="page-hero__subtitle">PhotonAssay&#8482; is a breakthrough technology that replaces traditional fire assay with faster, safer, and more sustainable elemental analysis.</p>
    </div>
  </section>

  <!-- ABOUT PHOTONASSAY -->
  <section class="section-light">
    <div class="container">
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-15); align-items: center;" class="reveal">
        <div>
          <p class="eyebrow">The Technology</p>
          <h2 style="font-size: 40px; margin-bottom: var(--space-4);">What is PhotonAssay&#8482;?</h2>
          <p style="margin-bottom: var(--space-4);">PhotonAssay is a non-destructive analytical technique that uses high-energy X-ray photons to determine the elemental composition of geological samples. Originally developed through CSIRO research, the technology was commercialised by Chrysos Corporation and is now deployed at mine sites and commercial laboratories around the world.</p>
          <p style="margin-bottom: var(--space-4);">Unlike traditional fire assay, which requires crushing, splitting, fluxing, and smelting a 50-gram sub-sample over many hours, PhotonAssay analyses the entire 500-gram sample in approximately two minutes. The sample remains intact and can be re-analysed or stored for future reference.</p>
          <p>The technology eliminates the use of lead-based fluxes and high-temperature furnaces, removing key occupational health hazards and producing zero scope 1 emissions from the assay process itself.</p>
        </div>
        <div class="placeholder-img" style="width: 100%; height: 480px;">PhotonAssay Unit &mdash; Product Image &mdash; 4:5</div>
      </div>
    </div>
  </section>

  <!-- TIMELINE -->
  <section class="section-offwhite">
    <div class="container">
      <div class="reveal">
        <p class="eyebrow">Our Journey</p>
        <h2 style="font-size: 40px; margin-bottom: var(--space-2);">Key milestones</h2>
        <p style="color: var(--grey-500); font-size: 14px; margin-bottom: var(--space-8);"><em>Placeholder content &mdash; Robyn to provide final timeline details from Collier's page 8 wireframe.</em></p>
      </div>
      <div class="timeline reveal">
        <div class="timeline__item">
          <div class="timeline__dot"></div>
          <div class="timeline__year">2008</div>
          <div class="timeline__title">CSIRO research begins</div>
          <div class="timeline__desc">Early-stage research into photon activation analysis for mineral characterisation begins at CSIRO's Minerals division.</div>
        </div>
        <div class="timeline__item">
          <div class="timeline__dot"></div>
          <div class="timeline__year">2014</div>
          <div class="timeline__title">Proof of concept validated</div>
          <div class="timeline__desc">Laboratory-scale testing demonstrates the viability of high-energy X-ray analysis for gold determination in geological matrices.</div>
        </div>
        <div class="timeline__item">
          <div class="timeline__dot"></div>
          <div class="timeline__year">2016</div>
          <div class="timeline__title">Chrysos Corporation formed</div>
          <div class="timeline__desc">Chrysos Corporation is established to commercialise the technology, with backing from CSIRO, RFC Ambrian, and mining industry investors.</div>
        </div>
        <div class="timeline__item">
          <div class="timeline__dot"></div>
          <div class="timeline__year">2018</div>
          <div class="timeline__title">First commercial deployment</div>
          <div class="timeline__desc">The first PhotonAssay unit is deployed at a commercial laboratory in Perth, Western Australia, marking the technology's entry into production use.</div>
        </div>
        <div class="timeline__item">
          <div class="timeline__dot"></div>
          <div class="timeline__year">2021</div>
          <div class="timeline__title">Global expansion accelerates</div>
          <div class="timeline__desc">Deployments expand across Australia, Africa, and the Americas. Chrysos lists on the ASX (ASX: C79).</div>
        </div>
        <div class="timeline__item">
          <div class="timeline__dot"></div>
          <div class="timeline__year">2024</div>
          <div class="timeline__title">Mine-site deployments scale</div>
          <div class="timeline__desc">The direct-to-mine-site operating model gains traction, with multiple tier-one miners deploying PhotonAssay on location for real-time grade control.</div>
        </div>
        <div class="timeline__item">
          <div class="timeline__dot"></div>
          <div class="timeline__year">2026</div>
          <div class="timeline__title">Next-generation platform announced</div>
          <div class="timeline__desc">PhotonAssay XN is announced, delivering higher throughput and expanded multi-element analysis capabilities including silver and copper.</div>
        </div>
      </div>
    </div>
  </section>

  <!-- CHRYSOS CORPORATION -->
  <section class="section-light">
    <div class="container">
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-15); align-items: center;" class="reveal">
        <div class="placeholder-img" style="width: 100%; height: 360px;">Chrysos Team / Office Image &mdash; 3:2</div>
        <div>
          <p class="eyebrow">Parent Company</p>
          <h2 style="font-size: 40px; margin-bottom: var(--space-4);">Chrysos Corporation</h2>
          <p style="margin-bottom: var(--space-4);">Chrysos Corporation Ltd (ASX: C79) is an Australian technology company headquartered in Adelaide, South Australia. The company was formed to commercialise PhotonAssay&#8482;, a transformative analytical technology originally developed through CSIRO research.</p>
          <p style="margin-bottom: var(--space-5);">Chrysos operates globally, with offices in Adelaide, Perth, and Vancouver, and a growing network of PhotonAssay deployments across multiple continents. The company is focused on making mineral analysis faster, safer, and more sustainable for the global resources industry.</p>
          <a href="https://chrysoscorp.com" target="_blank" class="arrow-link">Learn more about Chrysos Corporation {ARROW_DIAG_SVG}</a>
        </div>
      </div>
    </div>
  </section>

  <!-- CAREERS -->
  <section class="section-dark">
    <div class="container reveal" style="text-align: center; max-width: 640px;">
      <p class="eyebrow" style="justify-content: center; color: var(--grey-300);">Careers</p>
      <h2 style="color: var(--white); font-size: 40px; margin-bottom: var(--space-4);">Join the team transforming mineral analysis</h2>
      <p style="color: var(--grey-300); margin-bottom: var(--space-6);">We're growing a team of engineers, scientists, and industry specialists who are passionate about bringing new technology to the resources sector. If that sounds like you, we'd like to hear from you.</p>
      <a href="https://chrysoscorp.com/careers" target="_blank" class="btn btn--light">View Open Positions {ARROW_DIAG_SVG}</a>
    </div>
  </section>

  <!-- GET IN TOUCH CTA -->
  <section class="section-black cta-band">
    <div class="container reveal">
      <p class="eyebrow" style="justify-content: center; color: var(--grey-300);">Contact</p>
      <h2 style="color: var(--white); font-size: 48px;">Ready to learn more?</h2>
      <p style="color: var(--grey-300); max-width: 480px; margin: var(--space-3) auto var(--space-5);">Whether you're evaluating PhotonAssay for your operation or have a question about the technology, our team is here to help.</p>
      <a href="contact.html" class="btn btn--light">Get In Touch {ARROW_SVG}</a>
    </div>
  </section>
'''
    return page_shell("About Us", body, active_link="about")


# ── WRITE ALL PAGES ─────────────────────────────────────────────────────────

def main():
    pages = {
        'resources.html': build_resources,
        'resource-example.html': build_resource_example,
        'case-study-example.html': build_case_study_example,
        'ravenswood.html': build_ravenswood,
        'latest.html': build_latest,
        'event-example.html': build_event_example,
        'news-example.html': build_news_example,
        'about.html': build_about,
    }

    for filename, builder in pages.items():
        filepath = os.path.join(SITE_DIR, filename)
        html = builder()
        with open(filepath, 'w') as f:
            f.write(html)
        print(f"  Built {filename} ({len(html):,} chars)")

    print(f"\nAll {len(pages)} pages built successfully.")


if __name__ == '__main__':
    main()
