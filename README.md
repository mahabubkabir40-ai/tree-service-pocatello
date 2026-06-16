# Deploying Your Free Website

This folder contains a complete, static version of your WordPress website `treeservicepocatelloidaho.com` that you can host for **100% free**. 

The website has been set up with **Netlify Forms**, which means all submissions from your contact forms will automatically be sent to your email for free.

Here are the step-by-step instructions to get your website live:

---

## Step 1: Create a GitHub Repository

1. Go to [github.com](https://github.com/) and log in (or create a free account if you don't have one).
2. In the top-right corner, click the **`+`** icon and select **New repository**.
3. Name your repository (for example: `tree-service-pocatello`).
4. Keep the repository **Public** or **Private** (either is fine, but Public is standard for websites).
5. Do **not** check "Add a README", "Add .gitignore", or "Choose a license" (we already have these prepared).
6. Click **Create repository**.
7. Copy the repository URL (it will look like: `https://github.com/YOUR-USERNAME/tree-service-pocatello.git`).

---

## Step 2: Push Your Code to GitHub

Since I have already initialized Git and committed your files locally, you just need to run these final commands to link and upload your site to GitHub:

1. Open your terminal/command prompt.
2. Run these commands one by one (replace the URL with the one you copied in Step 1):
   ```bash
   git remote add origin https://github.com/YOUR-USERNAME/tree-service-pocatello.git
   git branch -M main
   git push -u origin main
   ```
   *Note: If GitHub asks you to log in during the `git push`, follow the prompts to authorize it.*

---

## Step 3: Deploy to Netlify (Free)

1. Go to [netlify.com](https://www.netlify.com/) and sign up for a free account. Select **Sign up with GitHub**.
2. Once logged in, click **Add new site** -> **Import an existing project**.
3. Select **GitHub** as your provider.
4. Authorize Netlify to access your GitHub account, and select your `tree-service-pocatello` repository.
5. In the Build settings, leave everything as default:
   - **Build command**: (Leave empty)
   - **Publish directory**: `.` (or leave empty)
6. Click **Deploy site**. Netlify will host your site in a few seconds and give you a random URL (like `https://subdomain.netlify.app`).

---

## Step 4: Map Your Custom Domain

To point `treeservicepocatelloidaho.com` to Netlify:

1. On your Netlify site dashboard, go to **Site settings** -> **Domain management** -> **Add custom domain**.
2. Enter `treeservicepocatelloidaho.com` and click **Save**.
3. Netlify will tell you that the domain is registered elsewhere. It will provide you with **DNS settings** (either nameservers or CNAME records).
4. Log into where you bought your domain (GoDaddy, Namecheap, Google Domains, etc.).
5. Go to the DNS settings and either:
   - **Option A (Recommended)**: Change the nameservers to Netlify's nameservers (Netlify lists these on your dashboard, e.g., `dns1.p01.nsone.net`). This lets Netlify handle the DNS and automatically renews a free SSL certificate.
   - **Option B**: Keep your current nameservers and add an `A` record pointing `@` to Netlify's IP address (`75.101.122.121`) and a `CNAME` record pointing `www` to your netlify app address (e.g. `your-app.netlify.app`).
6. Within a few hours, the domain will point to your new free website, and Netlify will generate a free SSL certificate (HTTPS) automatically!

---

## Step 5: Test and Enable Form Submissions

1. Once the site is live, go to your contact page and fill out the form.
2. Submit it. You should see a default Netlify success page.
3. Check your Netlify dashboard under the **Forms** tab to see your submission!
4. Go to **Form settings** in Netlify to configure email notifications so submissions are automatically forwarded to your email address (like `info@treeservicepocatelloidaho.com`).
