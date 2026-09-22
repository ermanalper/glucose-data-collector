FROM golang:alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN go build -o /app/dexcom-worker .

FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/dexcom-worker .
CMD ["./dexcom-worker"]