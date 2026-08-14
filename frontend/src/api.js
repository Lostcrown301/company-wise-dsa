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
