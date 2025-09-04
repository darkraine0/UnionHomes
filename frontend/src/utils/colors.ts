// Simplified color configuration for company consistency across all pages
export const getCompanyColor = (company: string) => {
  switch (company) {
    case 'DR Horton':
      return '#2563eb'; // Blue
    case 'UnionMain Homes':
      return '#e11d48'; // Red
    case 'M/I Homes':
      return '#9c27b0'; // Purple
    case 'Pacesetter Homes':
      return '#ff9800'; // Amber
    case 'Trophy Signature Homes':
      return '#2e7d32'; // Green
    case 'HistoryMaker Homes':
      return '#00a651'; // Green
    case 'K. Hovnanian Homes':
      return '#ff6b35'; // Orange
    case 'Highland Homes':
      return '#ec4899'; // Pink
    case 'Beazer Homes':
      return '#f43f5e'; // Rose
    case 'Redfin':
      return '#7c3aed'; // Violet
    case 'ChesmarHomes':
      return '#8b5cf6'; // Violet
    case 'PerryHomes':
    case 'Perry Homes':
      return '#6366f1'; // Indigo
    case 'CoventryHomes':
    case 'Coventry Homes':
      return '#0ea5e9'; // Sky
    case 'William Ryan Homes':
      return '#6366f1'; // Indigo
    case 'Rockwell Homes':
      return '#84cc16'; // Lime
    case 'American Legend Homes':
      return '#14b8a6'; // Teal
    case 'AshtonWoods Homes':
      return '#64748b'; // Slate
    case 'Bloomfield Homes':
      return '#d946ef'; // Fuchsia
    case 'Brightland Homes':
      return '#f43f5e'; // Rose
    case 'David Weekley Homes':
      return '#eab308'; // Yellow
    case 'Shaddock Homes':
      return '#78716c'; // Stone
    default:
      return '#888'; // Gray
  }
};
