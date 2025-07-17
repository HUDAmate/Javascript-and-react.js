package com.tiktubstudio.api;

import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.methods.*;
import org.apache.http.entity.ContentType;
import org.apache.http.entity.StringEntity;
import org.apache.http.entity.mime.MultipartEntityBuilder;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

/**
 * API Client untuk berkomunikasi dengan Python backend
 */
public class ApiClient {
    private static final Logger logger = LoggerFactory.getLogger(ApiClient.class);
    
    private final String baseUrl;
    private final CloseableHttpClient httpClient;
    private final Gson gson;
    
    public ApiClient(String baseUrl) {
        this.baseUrl = baseUrl.endsWith("/") ? baseUrl.substring(0, baseUrl.length() - 1) : baseUrl;
        this.httpClient = HttpClients.createDefault();
        this.gson = new Gson();
        
        logger.info("API Client initialized with base URL: {}", this.baseUrl);
    }
    
    /**
     * Check health status of backend
     */
    public boolean checkHealth() {
        try {
            String response = get("/api/health");
            JsonObject json = JsonParser.parseString(response).getAsJsonObject();
            return "healthy".equals(json.get("status").getAsString());
        } catch (Exception e) {
            logger.error("Health check failed", e);
            return false;
        }
    }
    
    /**
     * Upload video file
     */
    public ApiResponse uploadVideo(File videoFile) {
        try {
            logger.info("Uploading video: {}", videoFile.getName());
            
            HttpPost request = new HttpPost(baseUrl + "/api/upload");
            
            MultipartEntityBuilder builder = MultipartEntityBuilder.create();
            builder.addBinaryBody("video", videoFile, ContentType.DEFAULT_BINARY, videoFile.getName());
            
            HttpEntity multipart = builder.build();
            request.setEntity(multipart);
            
            HttpResponse response = httpClient.execute(request);
            String responseBody = EntityUtils.toString(response.getEntity());
            
            logger.debug("Upload response: {}", responseBody);
            
            return new ApiResponse(
                response.getStatusLine().getStatusCode() == 200,
                responseBody,
                response.getStatusLine().getStatusCode()
            );
            
        } catch (Exception e) {
            logger.error("Error uploading video", e);
            return new ApiResponse(false, "Error: " + e.getMessage(), 500);
        }
    }
    
    /**
     * Analyze video content
     */
    public ApiResponse analyzeVideo(String filePath) {
        try {
            logger.info("Analyzing video: {}", filePath);
            
            Map<String, String> payload = new HashMap<>();
            payload.put("file_path", filePath);
            
            String response = post("/api/analyze", gson.toJson(payload));
            return new ApiResponse(true, response, 200);
            
        } catch (Exception e) {
            logger.error("Error analyzing video", e);
            return new ApiResponse(false, "Error: " + e.getMessage(), 500);
        }
    }
    
    /**
     * Generate subtitles
     */
    public ApiResponse generateSubtitles(String filePath, String language) {
        try {
            logger.info("Generating subtitles for: {}", filePath);
            
            Map<String, String> payload = new HashMap<>();
            payload.put("file_path", filePath);
            payload.put("language", language);
            
            String response = post("/api/generate-subtitles", gson.toJson(payload));
            return new ApiResponse(true, response, 200);
            
        } catch (Exception e) {
            logger.error("Error generating subtitles", e);
            return new ApiResponse(false, "Error: " + e.getMessage(), 500);
        }
    }
    
    /**
     * Generate effects
     */
    public ApiResponse generateEffects(String filePath, String theme, String subtitleData) {
        try {
            logger.info("Generating effects for: {}", filePath);
            
            Map<String, Object> payload = new HashMap<>();
            payload.put("file_path", filePath);
            payload.put("theme", theme);
            if (subtitleData != null) {
                payload.put("subtitle_data", JsonParser.parseString(subtitleData));
            }
            
            String response = post("/api/generate-effects", gson.toJson(payload));
            return new ApiResponse(true, response, 200);
            
        } catch (Exception e) {
            logger.error("Error generating effects", e);
            return new ApiResponse(false, "Error: " + e.getMessage(), 500);
        }
    }
    
    /**
     * Start video processing
     */
    public ApiResponse processVideo(String filePath, Map<String, Object> config) {
        try {
            logger.info("Starting video processing: {}", filePath);
            
            Map<String, Object> payload = new HashMap<>();
            payload.put("file_path", filePath);
            payload.put("config", config);
            
            String response = post("/api/process", gson.toJson(payload));
            return new ApiResponse(true, response, 200);
            
        } catch (Exception e) {
            logger.error("Error processing video", e);
            return new ApiResponse(false, "Error: " + e.getMessage(), 500);
        }
    }
    
    /**
     * Get processing status
     */
    public ApiResponse getProcessingStatus(String jobId) {
        try {
            String response = get("/api/status/" + jobId);
            return new ApiResponse(true, response, 200);
            
        } catch (Exception e) {
            logger.error("Error getting processing status", e);
            return new ApiResponse(false, "Error: " + e.getMessage(), 500);
        }
    }
    
    /**
     * Get download results
     */
    public ApiResponse getDownloadResults(String jobId) {
        try {
            String response = get("/api/download/" + jobId);
            return new ApiResponse(true, response, 200);
            
        } catch (Exception e) {
            logger.error("Error getting download results", e);
            return new ApiResponse(false, "Error: " + e.getMessage(), 500);
        }
    }
    
    /**
     * Download specific file
     */
    public byte[] downloadFile(String jobId, String filename) {
        try {
            logger.info("Downloading file: {} for job: {}", filename, jobId);
            
            HttpGet request = new HttpGet(baseUrl + "/api/download-file/" + jobId + "/" + filename);
            HttpResponse response = httpClient.execute(request);
            
            if (response.getStatusLine().getStatusCode() == 200) {
                return EntityUtils.toByteArray(response.getEntity());
            } else {
                logger.error("Failed to download file: {}", response.getStatusLine());
                return null;
            }
            
        } catch (Exception e) {
            logger.error("Error downloading file", e);
            return null;
        }
    }
    
    /**
     * Get preview URL
     */
    public String getPreviewUrl(String jobId, String filename) {
        return baseUrl + "/api/preview/" + jobId + "/" + filename;
    }
    
    /**
     * List all jobs
     */
    public ApiResponse listJobs() {
        try {
            String response = get("/api/jobs");
            return new ApiResponse(true, response, 200);
            
        } catch (Exception e) {
            logger.error("Error listing jobs", e);
            return new ApiResponse(false, "Error: " + e.getMessage(), 500);
        }
    }
    
    /**
     * Cleanup job
     */
    public ApiResponse cleanupJob(String jobId) {
        try {
            logger.info("Cleaning up job: {}", jobId);
            
            HttpDelete request = new HttpDelete(baseUrl + "/api/cleanup/" + jobId);
            HttpResponse response = httpClient.execute(request);
            String responseBody = EntityUtils.toString(response.getEntity());
            
            return new ApiResponse(
                response.getStatusLine().getStatusCode() == 200,
                responseBody,
                response.getStatusLine().getStatusCode()
            );
            
        } catch (Exception e) {
            logger.error("Error cleaning up job", e);
            return new ApiResponse(false, "Error: " + e.getMessage(), 500);
        }
    }
    
    // Helper methods
    private String get(String endpoint) throws IOException {
        HttpGet request = new HttpGet(baseUrl + endpoint);
        request.setHeader("Content-Type", "application/json");
        
        HttpResponse response = httpClient.execute(request);
        return EntityUtils.toString(response.getEntity());
    }
    
    private String post(String endpoint, String jsonBody) throws IOException {
        HttpPost request = new HttpPost(baseUrl + endpoint);
        request.setHeader("Content-Type", "application/json");
        
        if (jsonBody != null) {
            request.setEntity(new StringEntity(jsonBody, ContentType.APPLICATION_JSON));
        }
        
        HttpResponse response = httpClient.execute(request);
        return EntityUtils.toString(response.getEntity());
    }
    
    private String put(String endpoint, String jsonBody) throws IOException {
        HttpPut request = new HttpPut(baseUrl + endpoint);
        request.setHeader("Content-Type", "application/json");
        
        if (jsonBody != null) {
            request.setEntity(new StringEntity(jsonBody, ContentType.APPLICATION_JSON));
        }
        
        HttpResponse response = httpClient.execute(request);
        return EntityUtils.toString(response.getEntity());
    }
    
    public void close() {
        try {
            httpClient.close();
        } catch (IOException e) {
            logger.error("Error closing HTTP client", e);
        }
    }
    
    /**
     * API Response wrapper class
     */
    public static class ApiResponse {
        private final boolean success;
        private final String body;
        private final int statusCode;
        
        public ApiResponse(boolean success, String body, int statusCode) {
            this.success = success;
            this.body = body;
            this.statusCode = statusCode;
        }
        
        public boolean isSuccess() {
            return success;
        }
        
        public String getBody() {
            return body;
        }
        
        public int getStatusCode() {
            return statusCode;
        }
        
        public JsonObject getJsonBody() {
            try {
                return JsonParser.parseString(body).getAsJsonObject();
            } catch (Exception e) {
                return new JsonObject();
            }
        }
    }
}