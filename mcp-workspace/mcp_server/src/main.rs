// Use the explicit service path to ensure the compiler finds the helper
use rmcp::service::mcp_server;
use rmcp::transport::io::stdio;
use rmcp_macros::tool;
use anyhow::Result;
use serde::{Deserialize, Serialize};
use std::env;
use reqwest::Client;

// --- Models ---

#[derive(Deserialize, Serialize)]
pub struct SearchResult {
    pub title: String,
    pub link: String,
    pub snippet: String,
}

#[derive(Deserialize, Serialize)]
pub struct SearchResponse {
    pub results: Vec<SearchResult>,
}

// --- API Client ---

async fn call_serper_api(query: &str) -> Result<Vec<SearchResult>> {
    let api_key = env::var("SERPER_API_KEY")
        .expect("SERPER_API_KEY must be set in the environment");
    
    let client = Client::new();
    let url = "https://google.serper.dev/search";
    let body = serde_json::json!({ "q": query });

    let resp = client.post(url)
        .header("X-API-KEY", api_key)
        .json(&body)
        .send()
        .await?
        .json::<serde_json::Value>()
        .await?;

    // FIX: Use .clone() to convert &Vec<Value> to Vec<Value> 
    // This solves the "ownership" error with serde_json::from_value
    let organic_vec = resp["organic"]
        .as_array()
        .map(|v| v.clone())
        .unwrap_or_default();
        
    let results: Vec<SearchResult> = serde_json::from_value(organic_vec)?;
    Ok(results)
}

// --- Tool Definition ---

// The #[tool] macro handles schema generation automatically.
// It detects "query" as the required input for this tool.
#[tool(name = "web_search", description = "Searches the internet for real-time information")]
pub async fn web_search(query: String) -> Result<SearchResponse> {
    let results = call_serper_api(&query).await?;
    Ok(SearchResponse { results })
}

// --- Server Entry Point ---

#[tokio::main]
async fn main() -> Result<()> {
    // Load .env variables
    dotenvy::dotenv().ok();

    // Call the builder helper from the service module.
    // This replaces RoleServer::new() and registration boilerplate.
    let server = mcp_server(web_search);

    // Use standard I/O for Claude Desktop compatibility
    let transport = stdio();

    // Execute the server loop
    server.run(transport).await
}
