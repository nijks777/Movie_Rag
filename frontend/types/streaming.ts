export interface StreamingPlatform {
  id: string;
  name: string;
  color: string;
  icon: string; // Emoji for simplicity
}

export const STREAMING_PLATFORMS: StreamingPlatform[] = [
  { id: 'netflix', name: 'Netflix', color: '#E50914', icon: 'N' },
  { id: 'disney', name: 'Disney+', color: '#0063E5', icon: 'D+' },
  { id: 'prime', name: 'Prime Video', color: '#00A8E1', icon: 'P' },
  { id: 'hulu', name: 'Hulu', color: '#1CE783', icon: 'H' },
  { id: 'apple', name: 'Apple TV+', color: '#000000', icon: 'A' },
  { id: 'hbo', name: 'Max', color: '#0000FF', icon: 'M' },
];

export function generateSearchLink(title: string, year?: string): string {
  const query = year ? `${title} ${year} watch online` : `${title} watch online`;
  return `https://www.google.com/search?q=${encodeURIComponent(query)}`;
}
