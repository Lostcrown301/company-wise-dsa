export async function getCompanies(search = "") {
  const url = new URL("/api/companies", window.location.origin);
  if (search) {
    url.searchParams.set("search", search);
  }
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Failed to fetch companies: ${response.statusText}`);
  }
  return response.json();
}

export async function getTopics(search = "") {
  const url = new URL("/api/topics", window.location.origin);
  if (search) {
    url.searchParams.set("search", search);
  }
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Failed to fetch topics: ${response.statusText}`);
  }
  return response.json();
}

export async function getQuestions(params = {}) {
  const url = new URL("/api/questions", window.location.origin);
  
  if (typeof params === 'string') {
    if (params) url.searchParams.set("search", params);
  } else {
    for (const [key, value] of Object.entries(params)) {
      if (value !== undefined && value !== null && value !== "") {
        url.searchParams.set(key, value);
      }
    }
  }

  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Failed to fetch questions: ${response.statusText}`);
  }
  return response.json();
}

export async function getRandomQuestions(params = {}) {
  const url = new URL("/api/questions/random", window.location.origin);
  
  for (const [key, value] of Object.entries(params)) {
    if (value !== undefined && value !== null && value !== "") {
      url.searchParams.set(key, value);
    }
  }

  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Failed to fetch random questions: ${response.statusText}`);
  }
  return response.json();
}

export async function getCompanyDetails(slug) {
  const url = new URL(`/api/companies/${slug}`, window.location.origin);
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Failed to fetch company details: ${response.statusText}`);
  }
  return response.json();
}

export async function getTopicDetails(slug) {
  const url = new URL(`/api/topics/${slug}`, window.location.origin);
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Failed to fetch topic details: ${response.statusText}`);
  }
  return response.json();
}

export async function trackVisitor(visitorId) {
  const url = new URL("/api/visitors", window.location.origin);
  try {
    await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ visitor_id: visitorId })
    });
  } catch (err) {
    console.error("Failed to track visitor", err);
  }
}

export async function trackAttempt(visitorId, slug) {
  const url = new URL("/api/attempts", window.location.origin);
  try {
    await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ visitor_id: visitorId, problem_slug: slug })
    });
  } catch (err) {
    console.error("Failed to track attempt", err);
  }
}

export async function trackSolve(visitorId, slug) {
  const url = new URL("/api/solves", window.location.origin);
  try {
    await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ visitor_id: visitorId, problem_slug: slug })
    });
  } catch (err) {
    console.error("Failed to track solve", err);
  }
}

export async function getStats() {
  const url = new URL("/api/stats", window.location.origin);
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Failed to fetch stats: ${response.statusText}`);
  }
  return response.json();
}
