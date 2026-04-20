# HubSpot Form Integration — Handover Note

This prototype contains **styled forms** that mirror the fields and options of Chrysos's live HubSpot forms. During WordPress development, these styled forms need to connect to HubSpot so submissions feed into the same automations.

## Forms in the prototype

### 1. PDF Download Form (`resource-example.html`)

Triggered by the "Download PDF" button. Modal form with these fields:

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Email | email | yes | |
| First name | text | yes | |
| Last Name | text | yes | |
| Global Region | select | yes | 6 options (Asia Pacific, Africa, Middle East, Europe, USA & Canada, Latin America & Caribbean) |
| What is the purpose of your enquiry? | select | yes | 3 options (PhotonAssay Technology / Chrysos Careers / Personal Interest) |
| What would you like to know or discuss? | textarea | no | |

**Robyn's HubSpot embed code (reference — not embedded in the prototype):**

```html
<script charset="utf-8" type="text/javascript" src="//js.hsforms.net/forms/embed/v2.js"></script>
<script>
hbspt.forms.create({
  portalId: "19622865",
  formId: "9a5cd10b-7037-4781-9770-aac028e0ded0",
  region: "na1"
});
</script>
```

## Why we didn't embed the HubSpot form directly

HubSpot's default form styling doesn't match the dark premium modal design. Embedding it would require heavy CSS overrides and would still feel inconsistent with the rest of the site.

## Recommended approach

Build the WordPress form to match the prototype visually, then POST submissions to HubSpot via the [HubSpot Forms API](https://legacydocs.hubspot.com/docs/methods/forms/submit_form):

```
POST https://api.hsforms.com/submissions/v3/integration/submit/19622865/9a5cd10b-7037-4781-9770-aac028e0ded0
```

This preserves the design AND captures leads in the same HubSpot form automations. No need to update any HubSpot-side automations.

## Other forms to look out for

- **Contact page** (`contact.html`) — may also need the same treatment
- **Newsletter sign-up** — currently on Homepage, Resources, and Latest pages (separate HubSpot form, Robyn still finalising)
