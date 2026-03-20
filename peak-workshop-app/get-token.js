// Get Shopify Admin API access token
const fetch = require('node-fetch');

const CLIENT_ID = '7d26042738e351ec17ef93b32b15c072';
const SHOP = 'peak-workshop.myshopify.com';

// Step 1: Build the OAuth URL
const scopes = 'write_products,read_products,write_content,read_content,write_themes,read_themes,read_orders,write_online_store_pages,read_online_store_pages,read_locales';
const redirectUri = 'https://example.com/auth/callback';
const nonce = Date.now().toString();

const authUrl = `https://${SHOP}/admin/oauth/authorize?client_id=${CLIENT_ID}&scope=${scopes}&redirect_uri=${encodeURIComponent(redirectUri)}&state=${nonce}`;

console.log('\n📋 Step 1: Visit this URL to authorize the app:\n');
console.log(authUrl);
console.log('\n📋 Step 2: After approving, you\'ll be redirected to example.com with a "code" parameter in the URL.');
console.log('Copy the entire URL and paste it here.\n');
