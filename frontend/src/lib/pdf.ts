import jsPDF from "jspdf";

export function generateSummaryPdf(before: any, after: any) {
  try {
    const pdf = new jsPDF({ unit: "mm", format: "a4", orientation: "portrait" });
    const margin = 15;
    const pageWidth = pdf.internal.pageSize.getWidth();
    const pageHeight = pdf.internal.pageSize.getHeight();
    let y = 20;

    pdf.setFontSize(18);
    pdf.text("EcoScale — Dashboard Summary", margin, y);
    y += 8;

    pdf.setFontSize(9);
    pdf.text(`Generated: ${new Date().toLocaleString()}`, margin, y);
    y += 8;

    // Configuration
    const cfg: any = (after && (after as any).config) || {};
    pdf.setFontSize(12);
    pdf.text("Configuration:", margin, y);
    y += 6;
    pdf.setFontSize(10);
    pdf.text(`- App Type: ${cfg.appType ?? "n/a"}`, margin + 4, y);
    y += 5;
    pdf.text(`- Traffic (RPS): ${cfg.trafficRps ?? "n/a"}`, margin + 4, y);
    y += 5;
    pdf.text(`- CPU Cores: ${cfg.cpuCores ?? "n/a"}`, margin + 4, y);
    y += 5;
    pdf.text(`- Memory (GB): ${cfg.memoryGb ?? "n/a"}`, margin + 4, y);
    y += 8;

    // Key metrics
    pdf.setFontSize(12);
    pdf.text("Key Metrics:", margin, y);
    y += 6;
    pdf.setFontSize(10);
    pdf.text(
      `- Before: CPU ${before.cpuUtilization}% | Energy ${Number((before.energyKwh * 1000).toFixed(2))} W | CO₂ ${Number((before.co2Kg * 1000).toFixed(2))} g`,
      margin + 4,
      y,
    );
    y += 6;
    pdf.text(
      `- After: CPU ${after.result.cpuUtilization}% | Energy ${Number((after.result.energyKwh * 1000).toFixed(2))} W | CO₂ ${Number((after.result.co2Kg * 1000).toFixed(2))} g`,
      margin + 4,
      y,
    );
    y += 6;
    pdf.text(`- Energy reduction: ${after.energyReduction}%`, margin + 4, y);
    y += 5;
    pdf.text(`- CO₂ reduction: ${after.co2Reduction}%`, margin + 4, y);
    y += 5;
    pdf.text(`- Green score: ${after.greenScore}`, margin + 4, y);
    y += 8;

    // Recommendations
    pdf.setFontSize(12);
    pdf.text("Recommendations:", margin, y);
    y += 6;
    pdf.setFontSize(10);
    if (after.recommendations && after.recommendations.length > 0) {
      after.recommendations.forEach((r: string) => {
        const lines = pdf.splitTextToSize(`- ${r}`, pageWidth - margin * 2 - 4);
        if (y + lines.length * 5 > pageHeight - margin) {
          pdf.addPage();
          y = margin;
        }
        pdf.text(lines, margin + 4, y);
        y += lines.length * 5 + 2;
      });
    } else {
      pdf.text("- No recommendations available", margin + 4, y);
      y += 6;
    }

    // Explainable AI summary (top features)
    const explanation = (after as any).explanation || {};
    const keys = Object.keys(explanation || {});
    if (keys.length > 0) {
      if (y > pageHeight - margin - 40) {
        pdf.addPage();
        y = margin;
      }
      pdf.setFontSize(12);
      pdf.text("Explainable AI - Feature Contributions:", margin, y);
      y += 6;
      pdf.setFontSize(10);
      keys.slice(0, 8).forEach((k) => {
        pdf.text(`- ${k}: ${Number(explanation[k]).toFixed(3)}`, margin + 4, y);
        y += 5;
      });
    }

    pdf.save("dashboard-summary.pdf");
  } catch (err) {
    // eslint-disable-next-line no-console
    console.error("Summary PDF failed", err);
  }
}
