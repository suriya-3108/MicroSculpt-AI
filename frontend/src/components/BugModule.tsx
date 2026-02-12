import { useState } from 'react';
import { AlertTriangle, CheckCircle, ArrowRight, Loader2, Play } from 'lucide-react';

interface BugModuleProps {
    onNext: () => void;
    projectData: any;
    setProjectData: (data: any) => void;
}

export function BugModule({ onNext, projectData, setProjectData }: BugModuleProps) {
    const [loading, setLoading] = useState(false);
    const [analyzed, setAnalyzed] = useState(false);
    const [bugs, setBugs] = useState<any[]>([]);
    const [summary, setSummary] = useState("");
    const [fixedCode, setFixedCode] = useState("");

    const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api';

    const runAnalysis = async () => {
        setLoading(true);
        try {
            const response = await fetch(`${API_URL}/analyze-bugs`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    code: projectData.code,
                    language: projectData.language
                }),
            });

            const data = await response.json();

            if (data.error) {
                alert("Error: " + data.error);
            } else {
                setBugs(data.issues || []);
                setSummary(data.summary || "");
                setFixedCode(data.fixed_code || projectData.code);
                setAnalyzed(true);
            }
        } catch (e) {
            console.error(e);
            alert("Failed to connect to API");
        } finally {
            setLoading(false);
        }
    };

    const applyFixes = () => {
        setProjectData({ ...projectData, code: fixedCode });
        alert("Fixes applied successfully!");
        onNext();
    };

    return (
        <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="border-b pb-4">
                <h2 className="text-2xl font-bold flex items-center">
                    <span className="bg-black text-white rounded-full w-8 h-8 flex items-center justify-center text-sm mr-3">2</span>
                    AI Bug Detection
                </h2>
                <p className="text-gray-500 mt-1 ml-11">Detect & Fix bugs using Gemini/Groq</p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 h-[500px]">
                {/* Code View */}
                <div className="border border-gray-200 rounded-xl overflow-hidden flex flex-col">
                    <div className="bg-gray-50 px-4 py-2 border-b border-gray-200 text-xs font-mono text-gray-500 uppercase">
                        Current Code
                    </div>
                    <div className="flex-1 bg-white p-4 overflow-auto font-mono text-sm whitespace-pre">
                        {projectData.code}
                    </div>
                </div>

                {/* Results View */}
                <div className="border border-gray-200 rounded-xl overflow-hidden flex flex-col bg-gray-50">
                    {!analyzed ? (
                        <div className="flex-1 flex flex-col items-center justify-center p-8 text-center">
                            <div className="bg-white p-4 rounded-full shadow-sm mb-4">
                                <AlertTriangle className="w-8 h-8 text-yellow-500" />
                            </div>
                            <h3 className="font-medium text-lg mb-2">Ready to Scan</h3>
                            <p className="text-gray-500 text-sm mb-6 max-w-xs">
                                Click the button below to let AI analyze your code for potential vulnerabilities and logic errors.
                            </p>
                            <button
                                onClick={runAnalysis}
                                disabled={loading}
                                className="flex items-center bg-blue-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-blue-700 transition-colors disabled:opacity-50"
                            >
                                {loading ? <Loader2 className="w-4 h-4 mr-2 animate-spin" /> : <Play className="w-4 h-4 mr-2" />}
                                {loading ? "Scanning..." : "Run AI Analysis"}
                            </button>
                        </div>
                    ) : (
                        <div className="flex-1 flex flex-col p-6 overflow-auto">
                            <h3 className="font-bold text-lg mb-4 flex items-center">
                                <AlertTriangle className="w-5 h-5 text-red-500 mr-2" />
                                Identified Issues ({bugs.length})
                            </h3>

                            <div className="space-y-3 flex-1 overflow-auto mb-4">
                                {bugs.map((bug: string, i: number) => (
                                    <div key={i} className="bg-white p-3 rounded-lg border border-gray-100 shadow-sm text-sm text-gray-700">
                                        • {bug}
                                    </div>
                                ))}
                                {bugs.length === 0 && (
                                    <div className="text-green-600 flex items-center">
                                        <CheckCircle className="w-4 h-4 mr-2" /> No major issues found.
                                    </div>
                                )}
                            </div>

                            <div className="bg-blue-50 p-4 rounded-lg text-sm text-blue-800 mb-6">
                                <strong>AI Summary:</strong> {summary}
                            </div>

                            <button
                                onClick={applyFixes}
                                className="w-full bg-black text-white py-3 rounded-lg font-medium hover:bg-gray-800 flex items-center justify-center transition-colors"
                            >
                                <CheckCircle className="w-4 h-4 mr-2" />
                                Apply Fixes & Continue
                            </button>
                        </div>
                    )}
                </div>
            </div>

            {analyzed && (
                <div className="flex justify-end">
                    <button onClick={onNext} className="text-sm text-gray-500 hover:text-gray-900 underline">
                        Skip this step
                    </button>
                </div>
            )}
        </div>
    );
}
