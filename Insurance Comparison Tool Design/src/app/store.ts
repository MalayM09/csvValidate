export type CoverageType = "health" | "term" | "car";
export type Priority = "low-premium" | "high-coverage" | "quick-claims";

export interface Policy {
  id: string;
  insurerName: string;
  insurerLogo: string;
  planName: string;
  type: CoverageType;
  priceMonthly: number;
  coverAmount: number; // in lacs or millions, keeping it generic
  roomRentLimit: string;
  claimSettlementRatio: number; // percentage
  features: string[];
}

export const MOCK_POLICIES: Policy[] = [
  {
    id: "p1",
    insurerName: "Care Health",
    insurerLogo: "https://images.unsplash.com/photo-1579621970588-a35d0e7ab9b6?auto=format&fit=crop&q=80&w=100&h=100", // using abstract/medical for logo
    planName: "Care Supreme",
    type: "health",
    priceMonthly: 850,
    coverAmount: 1000000,
    roomRentLimit: "No Limit",
    claimSettlementRatio: 95.2,
    features: ["No Copay", "Unlimited Restoration", "Free Annual Health Checkup"],
  },
  {
    id: "p2",
    insurerName: "HDFC ERGO",
    insurerLogo: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&q=80&w=100&h=100",
    planName: "Optima Secure",
    type: "health",
    priceMonthly: 1100,
    coverAmount: 2000000,
    roomRentLimit: "Single Private Room",
    claimSettlementRatio: 98.4,
    features: ["4X Coverage from Day 1", "No Sub-limits on Treatments", "Cashless everywhere"],
  },
  {
    id: "p3",
    insurerName: "Niva Bupa",
    insurerLogo: "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?auto=format&fit=crop&q=80&w=100&h=100",
    planName: "ReAssure 2.0",
    type: "health",
    priceMonthly: 920,
    coverAmount: 1500000,
    roomRentLimit: "Any Room Type",
    claimSettlementRatio: 91.5,
    features: ["Lock the clock (Premium doesn't increase by age)", "ReAssure+ Benefit", "LiveHealthy Discount"],
  },
  {
    id: "p4",
    insurerName: "Star Health",
    insurerLogo: "https://images.unsplash.com/photo-1532938911079-1b06ac7ceec7?auto=format&fit=crop&q=80&w=100&h=100",
    planName: "Comprehensive",
    type: "health",
    priceMonthly: 780,
    coverAmount: 500000,
    roomRentLimit: "Single Standard A/C",
    claimSettlementRatio: 89.9,
    features: ["Bariatric Surgery Cover", "Outpatient Dental/Ophthalmic", "Delivery Expenses Cover"],
  },
  {
    id: "p5",
    insurerName: "ICICI Lombard",
    insurerLogo: "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&q=80&w=100&h=100",
    planName: "Health AdvantEdge",
    type: "health",
    priceMonthly: 1300,
    coverAmount: 3000000,
    roomRentLimit: "No Limit",
    claimSettlementRatio: 97.1,
    features: ["Global Cover included", "Maternity Benefit", "Air Ambulance Cover"],
  }
];

// Helper to format currency
export const formatCurrency = (value: number) => {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0,
  }).format(value);
};
