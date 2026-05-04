import axios from "axios";

export class OrvionClient {
  constructor({ apiKey, token, baseUrl = "http://localhost:3000" } = {}) {
    if (!apiKey) throw new Error("apiKey is required");

    this.apiKey = apiKey;
    this.token = token || "test";
    this.baseUrl = baseUrl;

    this.http = axios.create({
      baseURL: baseUrl,
      timeout: 10000,
      headers: {
        "x-api-key": this.apiKey,
        "authorization": `Bearer ${this.token}`,
        "content-type": "application/json",
      },
    });

    // Add response interceptor for error handling
    this.http.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response) {
          const err = new Error(error.response.data?.error || "API Error");
          err.status = error.response.status;
          err.data = error.response.data;
          throw err;
        }
        throw error;
      }
    );
  }

  /**
   * Make a generic API call
   */
  async call(path = "/v1/ping", body = {}) {
    const { data } = await this.http.post(path, body);
    return data;
  }

  /**
   * Send a payment via Circle/Arc
   */
  async pay({ amount, recipient }) {
    if (!amount || !recipient) {
      throw new Error("amount and recipient are required");
    }

    const { data } = await this.http.post("/v1/pay", {
      apiKey: this.apiKey,
      amount: parseFloat(amount),
      recipient,
    });

    return data;
  }

  /**
   * Check service health
   */
  async health() {
    const { data } = await this.http.get("/health");
    return data;
  }

  /**
   * Get current usage stats
   */
  async getUsage() {
    const { data } = await this.http.get(`/v1/usage/${this.apiKey}`);
    return data;
  }

  /**
   * Get billing information
   */
  async getBilling() {
    const { data } = await this.http.get(`/v1/billing/${this.apiKey}`);
    return data;
  }

  /**
   * Get payment status
   */
  async getPaymentStatus(paymentId) {
    const { data } = await this.http.get(`/v1/payment/${paymentId}`);
    return data;
  }

  /**
   * List recent payments
   */
  async listPayments(limit = 10) {
    const { data } = await this.http.get(`/v1/payments?limit=${limit}`);
    return data;
  }
}

export default OrvionClient;
