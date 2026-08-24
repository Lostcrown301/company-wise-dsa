import fs from 'fs';

async function fetchWithTimeout(url, options = {}) {
  const timeout = options.timeout || 10000;
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeout);
  
  const response = await fetch(url, {
    ...options,
    signal: controller.signal  
  });
  clearTimeout(id);
  
  return response;
}

async function generateSitemap() {
  const baseUrl = 'https://company-dsa-practice-tau.vercel.app';
  const apiUrl = 'https://company-wise-dsa.onrender.com/api';
  
  let companies = [];
  let topics = [];
  let apiSuccess = false;

  try {
    console.log('Fetching companies...');
    const companiesRes = await fetchWithTimeout(apiUrl + '/companies?limit=1000', { timeout: 10000 });
    if (!companiesRes.ok) throw new Error('Companies API error: ' + companiesRes.status);
    const companiesData = await companiesRes.json();
    companies = companiesData.items || companiesData;
    if (!Array.isArray(companies)) throw new Error('Companies response is not an array');

    console.log('Fetching topics...');
    const topicsRes = await fetchWithTimeout(apiUrl + '/topics?limit=1000', { timeout: 10000 });
    if (!topicsRes.ok) throw new Error('Topics API error: ' + topicsRes.status);
    const topicsData = await topicsRes.json();
    topics = topicsData.items || topicsData;
    if (!Array.isArray(topics)) throw new Error('Topics response is not an array');

    console.log('Fetched ' + companies.length + ' companies and ' + topics.length + ' topics.');
    apiSuccess = true;
  } catch (err) {
    console.warn('API fetch failed, falling back to static routes only:', err.message);
  }

  const generatedUrls = new Set();
  let sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n';
  
  const addUrl = (path, priority) => {
    const fullUrl = baseUrl + path;
    if (!generatedUrls.has(fullUrl)) {
      generatedUrls.add(fullUrl);
      sitemap += '  <url>\n    <loc>' + fullUrl + '</loc>\n    <changefreq>weekly</changefreq>\n    <priority>' + priority + '</priority>\n  </url>\n';
    }
  };

  const staticRoutes = ['/', '/companies', '/topics', '/questions', '/practice'];
  for (const route of staticRoutes) {
    const priority = route === '/' ? '1.0' : '0.8';
    addUrl(route, priority);
  }

  if (apiSuccess) {
    companies.forEach(company => {
      if (company && company.slug) {
        addUrl('/companies/' + encodeURIComponent(company.slug), '0.7');
      }
    });

    topics.forEach(topic => {
      if (topic && topic.slug) {
        addUrl('/topics/' + encodeURIComponent(topic.slug), '0.7');
      }
    });
  }

  sitemap += '</urlset>\n';

  try {
    fs.writeFileSync('./public/sitemap.xml', sitemap);
    console.log('Successfully generated public/sitemap.xml with ' + generatedUrls.size + ' URLs.');
  } catch (err) {
    console.error('Failed to write sitemap.xml:', err);
    process.exit(1); 
  }
}

generateSitemap();
