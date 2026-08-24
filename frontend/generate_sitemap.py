import requests
import json
import os

base_url = "https://company-dsa-practice-tau.vercel.app"
api_url = "https://company-wise-dsa.onrender.com/api"

def generate():
    print("Fetching companies...")
    try:
        res = requests.get(f"{api_url}/companies?limit=1000")
        res.raise_for_status()
        comp_data = res.json()
        companies = comp_data.get('items', comp_data) if isinstance(comp_data, dict) else comp_data
    except Exception as e:
        print(f"Error fetching companies: {e}")
        companies = []

    print("Fetching topics...")
    try:
        res = requests.get(f"{api_url}/topics?limit=1000")
        res.raise_for_status()
        top_data = res.json()
        topics = top_data.get('items', top_data) if isinstance(top_data, dict) else top_data
    except Exception as e:
        print(f"Error fetching topics: {e}")
        topics = []

    print(f"Fetched {len(companies)} companies and {len(topics)} topics.")

    sitemap = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{base_url}/</loc>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>{base_url}/companies</loc>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>{base_url}/topics</loc>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>{base_url}/questions</loc>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>{base_url}/practice</loc>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
'''

    for company in companies:
        if isinstance(company, dict) and 'slug' in company:
            sitemap += f'''  <url>
    <loc>{base_url}/companies/{company['slug']}</loc>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>
'''

    for topic in topics:
        if isinstance(topic, dict) and 'slug' in topic:
            sitemap += f'''  <url>
    <loc>{base_url}/topics/{topic['slug']}</loc>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>
'''

    sitemap += "</urlset>\n"

    with open("public/sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap)
    
    print("Successfully generated public/sitemap.xml")

if __name__ == "__main__":
    generate()
