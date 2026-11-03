// Whop embedded checkout, compiled into funnel/whop-checkout.js so it runs on plain pages (GHL, GitHub Pages).
// Rebuild after any change:  cd whop-checkout && npm install && npm run build
import React from "react";
import { createRoot } from "react-dom/client";
import { loadWhop } from "@whop/elements";
import { Checkout, CheckoutElement, WhopElements } from "@whop/elements-react";

// The component from Whop, with the page's language, colours and redirects added
export function EmbeddedCheckout({ plan, returnUrl, onComplete }) {
  return (
    <WhopElements
      elements={loadWhop()}
      locale="es"
      appearance={{ theme: { appearance: "light", accentColor: "crimson", grayColor: "mauve" } }}
    >
      <Checkout plan={plan} returnUrl={returnUrl} onComplete={onComplete}>
        <CheckoutElement />
      </Checkout>
    </WhopElements>
  );
}

// page.js calls this once the visitor nears the prices
window.JCWhopCheckout = {
  mount(el, options) {
    createRoot(el).render(<EmbeddedCheckout {...options} />);
  },
};
