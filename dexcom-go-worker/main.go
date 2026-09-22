package main

import (
	"bytes"
	"context"
	"encoding/json"
	"log"
	"net/http"
	"os"
	"time"

	dexcomshare "github.com/mntndev/dexcom-share"
)

type PushPayload struct {
	Value       int    `json:"value"`
	TrendSymbol string `json:"trend_symbol"`
}

func main() {
	username := os.Getenv("DEXCOM_USERNAME")
	password := os.Getenv("DEXCOM_PASSWORD")
	webhookURL := os.Getenv("WEBHOOK_URL")
	apiKey := os.Getenv("API_KEY")

	if username == "" || password == "" || webhookURL == "" || apiKey == "" {
		log.Fatal("Missing env. variables! Define all variables.")
	}

	ctx := context.Background()
	client := login(ctx, username, password)

	for {
		entries, err := client.ReadGlucose(ctx, 10, 1)
		
		if err != nil {
			log.Printf("Data fetch : %v", err)
			client = login(ctx, username, password) //re-login
		} else if len(entries) > 0 {
			entry := entries[0]
			
			
			trendArrow := entry.Trend.Arrow()
			glucoseValue := entry.Value
			
			log.Printf(" %d mg/dL, %s", glucoseValue, trendArrow)
			pushToFastAPI(webhookURL, apiKey, glucoseValue, trendArrow)
		}

		// wait for 5 mins
		time.Sleep(5 * time.Minute)
	}
}

func login(ctx context.Context, username, password string) *dexcomshare.Client {
	log.Println("Logging into Dexcom OUS server...")
	client, err := dexcomshare.NewClient(ctx, username, password,
		dexcomshare.WithBaseURL(dexcomshare.BaseURLOutsideUS),
	)
	if err != nil {
		log.Fatalf("Critical login error: %v", err)
	}
	log.Println("Login successful!")
	return client
}

func pushToFastAPI(webhookURL, apiKey string, value int, trend string) {
	payload := PushPayload{
		Value:       value,
		TrendSymbol: trend,
	}
	
	jsonData, _ := json.Marshal(payload)
	req, _ := http.NewRequest("POST", webhookURL, bytes.NewBuffer(jsonData))
	
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("X-API-Key", apiKey)
	
	client := &http.Client{Timeout: 10 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		log.Printf("Webhook not found: %v", err)
		return
	}
	defer resp.Body.Close()
	
	if resp.StatusCode == 200 || resp.StatusCode == 201 {
		log.Println("✅ Data sent to FastAPI Webhook.")
	} else {
		log.Printf("❌ FastAPI did not return HTTP 200/201. Status Code: %d", resp.StatusCode)
	}
}