// Everything Mariam-specific lives here. Fill in and every page picks it up.
const CONFIG = {
  leadUrl: "https://app.worktimealliance.com/api/accountant/office/lead",  // WorkTime endpoint: creates a card in the pipeline and e-mails Mariam; on failure the form falls back to e-mail
  bookingUrl: "https://app.worktimealliance.com/accountant/book/muk-accounting",  // public booking page from the WorkTime cabinet; empty = "Book a call" scrolls to the request form
  email: "mariamkrevskaia@gmail.com",    // where form requests are addressed
  phone: "+1 (564) 999-0089",            // mobile
  phoneOffice: "(253) 655-0555",         // office line
  address: "19115 68th Ave S, H-109, Kent, WA 98032",
  hours: {
    en: "Tax season (January–April): 10 AM – 6 PM · Rest of the year: by appointment",
    ru: "Налоговый сезон (январь–апрель): 10:00–18:00 · В остальное время — по записи",
  },
};
