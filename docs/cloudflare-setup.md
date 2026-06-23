# Cloudflare Setup

Add the domain to Cloudflare, update registrar nameservers, then add host-supplied A or CNAME records. Use Full or Full Strict SSL when the origin has a certificate. Cache static assets, but bypass `/admin/`, `/accounts/`, `/cart/`, `/checkout/`, `/payments/`, and `/orders/`.

Keep proxy off during host verification if the provider requires direct DNS visibility. Configure the origin server or proxy layer to preserve real visitor IP headers.
