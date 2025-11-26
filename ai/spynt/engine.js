function calculateCharisma(metrics) {
  let charisma = 0;
  if (metrics.error) return 500; // neutral default

  charisma += Math.min(((metrics.resonanceScore || 30) / 100) * 600, 600);
  charisma += Math.min(((metrics.grassrootsSupport || 10000) / 10_000_000) * 600, 600);
  charisma += Math.min(Math.log10(metrics.audienceSize || 1000) * 70, 450);
  charisma += Math.min(((metrics.deepViewCount || 100000) / 50_000_000) * 600, 450);
  charisma += Math.min(((metrics.engagementScore || 20) / 100) * 400, 300);
  charisma += Math.min(
    (((metrics.referenceCount || 50) / 5000) * 300) +
    (((metrics.trustScore || 50) / 100) * 300),
    300
  );

  return Math.round(Math.min(charisma, 3000));
}
