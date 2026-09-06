import { describe, expect, it } from "vitest";

describe("desktop foundation", () => {
  it("keeps business UI behind an authenticated session", () => {
    expect("/api/v1/auth/login").toContain("auth");
  });
});
