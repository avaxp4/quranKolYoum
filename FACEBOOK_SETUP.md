# How to Get Facebook Credentials 🔑

To let the bot post on your page, you need a **Page ID** and a **Long-Lived Access Token**.

### Step 1: Create an App
1. Go to [Meta for Developers](https://developers.facebook.com/).
2. Log in with your Facebook account and click **"My Apps"**.
3. Click **"Create App"**.
4. Select **"Other"** (or "Business") -> **Next**.
5. Select **"Business"** -> **Next**.
6. Enter an App Name (e.g., "QuranBot") and click **Create App**.

### Step 2: Generate Access Token
1. In your App Dashboard, go to **Tools** -> **Graph API Explorer**.
2. On the right side:
   - **Meta App:** Select the app you just created.
   - **User or Page:** Select **"Page Access Token"** (Select your Facebook Page from the dropdown).
   - **Permissions:** Add the following permissions:
     - `pages_manage_posts`
     - `pages_read_engagement`
     - `pages_manage_metadata`
3. Click **"Generate Access Token"**.
4. Copy the generated token.

### Step 3: Get Page ID
1. While in the **Graph API Explorer**, look at the query field.
2. It usually says `me?fields=id,name`. Click **Submit**.
3. You will see your Page's **ID** in the result. Copy it. (This is your `FACEBOOK_PAGE_ID`).

### Step 4: Make the Token Long-Lived (Important!)
The token from Step 2 expires in 1 hour. You need a permanent one (60 days).
1. Go to the [Access Token Debugger](https://developers.facebook.com/tools/debug/accesstoken/).
2. Paste your token and click **Debug**.
3. Scroll down and click **"Extend Access Token"**.
4. A new, long token will appear. **Copy this new token**.
5. This is your `FACEBOOK_ACCESS_TOKEN`.

> **Note:** You will need to refresh this token every 60 days by repeating Step 4.

---

## Common Issues

Here are solutions to the most common problems you might face:

### 1. "I can see the posts, but others cannot!"
If the posts appear on your Page when **you** look at them, but your friends say the Page looks empty:
*   **Cause:** Your Facebook App is likely still in **"Development Mode"**.
*   **Solution:**
    1. Go to your [App Dashboard](https://developers.facebook.com/apps/).
    2. Look for the toggle button at the top (it says **In Development**).
    3. Switch it to **Live**.
    *   *Note: If Facebook asks for "Business Verification" or "App Review" to switch to Live, please contact me for a workaround.*

### 2. "Error: Session has expired or is invalid"
*   **Cause:** Your Access Token has expired (it usually lasts 60 days).
*   **Solution:** You simply need to generate a new token following the steps in this guide again and update your GitHub Secret.

---

## Still Stuck?

**Please Note:** Meta (Facebook) frequently changes their Developer Interface. If you find that the screenshots or steps above don't match exactly what you see, or if you encounter errors like *"Submit for Review"* or *"Invalid Permissions"*:

**Don't worry, this is normal!**

I am available to guide you through this step personally. Please feel free to contact me immediately:

- **Telegram:** [@Avax43](https://t.me/Avax43)

_I will help you generate the token in a few minutes._