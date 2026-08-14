/**
 * PDF export, print, copy, and share utilities.
 */
import jsPDF from 'jspdf';

/**
 * Generate and download a PDF report.
 */
export const downloadPDF = (result, formData) => {
  const doc = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' });
  const pageW = doc.internal.pageSize.getWidth();
  const margin = 20;
  let y = 20;

  const line = () => {
    doc.setDrawColor(79, 172, 254);
    doc.setLineWidth(0.3);
    doc.line(margin, y, pageW - margin, y);
    y += 6;
  };

  // Title
  doc.setFillColor(5, 11, 20);
  doc.rect(0, 0, pageW, 40, 'F');
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(18);
  doc.setTextColor(79, 172, 254);
  doc.text('AI Mental Health Prediction Report', margin, 18);
  doc.setFontSize(9);
  doc.setTextColor(148, 175, 201);
  doc.text(`Generated: ${new Date().toLocaleString()}`, margin, 28);
  y = 50;

  // Result section
  doc.setTextColor(30, 30, 30);
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(13);
  doc.text('Prediction Results', margin, y);
  y += 4;
  line();

  const addRow = (label, value) => {
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(10);
    doc.setTextColor(90, 122, 153);
    doc.text(label, margin, y);
    doc.setFont('helvetica', 'normal');
    doc.setTextColor(30, 30, 30);
    doc.text(String(value), margin + 60, y);
    y += 8;
  };

  addRow('Mental Health Condition:', result.condition);
  addRow('Severity:', result.severity);
  addRow('Confidence:', `${result.confidence}%`);
  addRow('Prediction Time:', result.prediction_time);
  y += 2;

  // Treatment
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(10);
  doc.setTextColor(90, 122, 153);
  doc.text('Treatment:', margin, y);
  doc.setFont('helvetica', 'normal');
  doc.setTextColor(30, 30, 30);
  const treatmentLines = doc.splitTextToSize(result.treatment, pageW - margin * 2 - 60);
  doc.text(treatmentLines, margin + 60, y);
  y += treatmentLines.length * 6 + 6;

  line();

  // Recommendations
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(13);
  doc.setTextColor(30, 30, 30);
  doc.text('Wellness Recommendations', margin, y);
  y += 4;
  line();

  result.recommendations.forEach((rec, i) => {
    doc.setFont('helvetica', 'normal');
    doc.setFontSize(10);
    doc.setTextColor(50, 50, 50);
    const lines = doc.splitTextToSize(`${i + 1}. ${rec}`, pageW - margin * 2);
    doc.text(lines, margin, y);
    y += lines.length * 6 + 3;
  });

  // AI Suggestion
  if (result.gemini_suggestion) {
    y += 4;
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(13);
    doc.setTextColor(30, 30, 30);
    doc.text('AI Wellness Suggestion', margin, y);
    y += 4;
    line();
    doc.setFont('helvetica', 'normal');
    doc.setFontSize(10);
    doc.setTextColor(50, 50, 50);
    const aiLines = doc.splitTextToSize(result.gemini_suggestion, pageW - margin * 2);
    doc.text(aiLines, margin, y);
    y += aiLines.length * 6;
  }

  // Footer
  const pageH = doc.internal.pageSize.getHeight();
  doc.setFont('helvetica', 'italic');
  doc.setFontSize(8);
  doc.setTextColor(150, 150, 150);
  doc.text('This report is for informational purposes only. Please consult a qualified mental health professional.', margin, pageH - 12);

  doc.save(`mental-health-report-${Date.now()}.pdf`);
};

/**
 * Print the results section.
 */
export const printReport = (result) => {
  const content = buildTextReport(result);
  const printWindow = window.open('', '_blank', 'width=700,height=900');
  printWindow.document.write(`
    <html><head><title>Mental Health Report</title>
    <style>
      body { font-family: Arial, sans-serif; padding: 32px; color: #111; }
      h1 { color: #4facfe; border-bottom: 2px solid #4facfe; padding-bottom: 8px; }
      h2 { color: #2d4a6e; margin-top: 24px; }
      p { line-height: 1.7; }
      li { margin-bottom: 6px; }
    </style></head>
    <body><pre style="font-family:inherit;white-space:pre-wrap">${content}</pre></body></html>
  `);
  printWindow.document.close();
  printWindow.print();
};

/**
 * Copy the report text to clipboard.
 */
export const copyReport = async (result) => {
  const content = buildTextReport(result);
  await navigator.clipboard.writeText(content);
};

/**
 * Share the result using the Web Share API or fall back to copy.
 */
export const shareReport = async (result) => {
  const content = buildTextReport(result);
  if (navigator.share) {
    await navigator.share({
      title: 'My Mental Health Report',
      text: content,
    });
  } else {
    await copyReport(result);
  }
};

function buildTextReport(result) {
  const date = new Date().toLocaleString();
  const recs = result.recommendations?.map((r, i) => `  ${i + 1}. ${r}`).join('\n') || '';
  return `
AI MENTAL HEALTH PREDICTION REPORT
Generated: ${date}
${'='.repeat(50)}

PREDICTION RESULTS
------------------
Condition:       ${result.condition}
Severity:        ${result.severity}
Confidence:      ${result.confidence}%
Treatment:       ${result.treatment}
Prediction Time: ${result.prediction_time}

RECOMMENDATIONS
---------------
${recs}

AI WELLNESS SUGGESTION
----------------------
${result.gemini_suggestion || 'N/A'}

--------------------------------------------------
DISCLAIMER: This report is for informational use only.
Please consult a qualified mental health professional.
`.trim();
}
