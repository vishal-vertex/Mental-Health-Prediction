import { useEffect, useRef } from 'react';
import toast from 'react-hot-toast';
import { usePrediction } from '../../hooks/usePrediction';
import { usePredictionHistory } from '../../hooks/usePredictionHistory';
import { downloadPDF, printReport, shareReport } from '../../utils/pdfExport';
import PredictionForm from '../../components/PredictionForm/PredictionForm';
import ResultCard from '../../components/ResultCard/ResultCard';
import Loading from '../../components/Loading/Loading';
import './Predict.css';

export default function Predict() {
  const { formData, errors, result, loading, apiError, updateField, submit, resetForm } = usePrediction();
  const { saveToHistory } = usePredictionHistory();
  const resultRef = useRef(null);

  useEffect(() => {
    if (apiError) {
      toast.error(apiError);
    }
  }, [apiError]);

  const handleSubmit = async () => {
    const success = await submit();
    if (success) {
      toast.success('Assessment generated successfully!');
      // Assuming result state updates asynchronously, we'll wait for the next render to scroll
      setTimeout(() => {
        if (resultRef.current) {
          resultRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }, 100);
    } else if (!apiError) {
      toast.error('Please fix the errors in the form.');
    }
  };

  // In a real app we'd trigger saveToHistory after successful submit, but we need the new result.
  // We'll use a useEffect to detect new results.
  useEffect(() => {
    if (result) {
      saveToHistory(result, formData);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [result]); // Only run when result changes

  const handleReset = () => {
    resetForm();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <main className="page-predict animate-fadeIn">
      <div className="container">
        <header className="page-header text-center">
          <span className="section-label">Assessment</span>
          <h1 className="section-title">Evaluate Your Well-being</h1>
          <p className="section-subtitle mx-auto">
            Please answer honestly for the most accurate prediction. This assessment takes about 2 minutes.
          </p>
        </header>

        {loading ? (
          <Loading text="The Random Forest models are analyzing your profile..." />
        ) : (
          <PredictionForm
            formData={formData}
            updateField={updateField}
            errors={errors}
            loading={loading}
            onSubmit={handleSubmit}
          />
        )}

        {/* Results Dashboard */}
        {result && (
          <div ref={resultRef} className="dashboard-section animate-fadeIn">
            <div className="divider"></div>

            <div className="dashboard-header">
              <h2 className="section-title">Assessment Results</h2>
              <div className="dashboard-actions">
                <button className="btn btn-secondary btn-sm" onClick={() => downloadPDF(result)}>
                  Download PDF
                </button>
                <button className="btn btn-secondary btn-sm" onClick={() => printReport(result)}>
                  Print Report
                </button>
                <button className="btn btn-secondary btn-sm" onClick={() => shareReport(result)}>
                  Share
                </button>
                <button className="btn btn-ghost btn-sm" onClick={handleReset}>
                  Start Over
                </button>
              </div>
            </div>

            <ResultCard result={result} />
          </div>
        )}
      </div>
    </main>
  );
}
