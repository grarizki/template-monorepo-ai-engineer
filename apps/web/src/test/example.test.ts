import { describe, it, expect } from "vitest";

describe("Example", () => {
  it("works", () => {
    expect(1 + 1).toBe(2);
  });

  it("string operations", () => {
    expect("hello".toUpperCase()).toBe("HELLO");
  });
});
