import { useState, useRef } from 'react';
import { Upload, FileCode, ArrowRight, AlertCircle, Loader2 } from 'lucide-react';

interface InputModuleProps {
    onNext: () => void;
    projectData: any;
    setProjectData: (data: any) => void;
}

export function InputModule({ onNext, projectData, setProjectData }: InputModuleProps) {
    const [dragActive, setDragActive] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const fileInputRef = useRef<HTMLInputElement>(null);

    const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api';

    const handleFiles = async (file: File) => {
        const text = await file.text();
        setProjectData({ ...projectData, code: text, filename: file.name });
    };

    const onDrag = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true);
        } else if (e.type === "dragleave") {
            setDragActive(false);
        }
    };

    const onDrop = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFiles(e.dataTransfer.files[0]);
        }
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            handleFiles(e.target.files[0]);
        }
    };

    const analyzeCode = async () => {
        if (!projectData.code) {
            setError("Please input some code first.");
            return;
        }

        setLoading(true);
        setError(null);

        try {
            const response = await fetch(`${API_URL}/parse`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    code: projectData.code,
                    fileName: projectData.filename || 'snippet.py'
                }),
            });

            const data = await response.json();

            if (response.ok) {
                setProjectData({
                    ...projectData,
                    language: data.language,
                    functions: data.functions
                });
                onNext();
            } else {
                setError(data.error || "Analysis failed");
            }
        } catch (err) {
            setError("Failed to connect to backend. Make sure the server is running.");
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="border-b pb-4">
                <h2 className="text-2xl font-bold flex items-center">
                    <span className="bg-black text-white rounded-full w-8 h-8 flex items-center justify-center text-sm mr-3">1</span>
                    Code Input & Analysis
                </h2>
                <p className="text-gray-500 mt-1 ml-11">Upload your source file or paste code directly.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Upload Area */}
                <div
                    className={`border-2 border-dashed rounded-xl p-8 flex flex-col items-center justify-center text-center transition-colors
            ${dragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-300'}`}
                    onDragEnter={onDrag}
                    onDragLeave={onDrag}
                    onDragOver={onDrag}
                    onDrop={onDrop}
                >
                    <div className="bg-gray-100 p-4 rounded-full mb-4">
                        <Upload className="w-8 h-8 text-gray-600" />
                    </div>
                    <h3 className="font-semibold text-lg">Drag & Drop your file</h3>
                    <p className="text-sm text-gray-500 mt-2 mb-6">Supports Python, JavaScript, Java, Go, C#</p>

                    <button
                        onClick={() => fileInputRef.current?.click()}
                        className="px-4 py-2 bg-white border border-gray-300 rounded-lg text-sm font-medium hover:bg-gray-50 shadow-sm"
                    >
                        Browse Files
                    </button>
                    <input
                        ref={fileInputRef}
                        type="file"
                        className="hidden"
                        onChange={handleChange}
                        accept=".py,.js,.ts,.java,.go,.cs"
                    />
                </div>

                {/* Text Area */}
                <div className="flex flex-col h-full">
                    <textarea
                        className="flex-1 w-full p-4 border border-gray-200 rounded-xl font-mono text-sm bg-gray-50 focus:ring-2 focus:ring-blue-500 focus:outline-none resize-none"
                        placeholder="Or paste your code here..."
                        value={projectData.code}
                        onChange={(e) => setProjectData({ ...projectData, code: e.target.value })}
                    />
                </div>
            </div>

            {error && (
                <div className="bg-red-50 text-red-600 p-4 rounded-lg flex items-center text-sm">
                    <AlertCircle className="w-4 h-4 mr-2" />
                    {error}
                </div>
            )}

            <div className="flex justify-end pt-4">
                <button
                    onClick={analyzeCode}
                    disabled={loading || !projectData.code}
                    className="flex items-center bg-black text-white px-6 py-3 rounded-lg font-medium hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                >
                    {loading ? (
                        <>
                            <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                            Analyzing Syntax...
                        </>
                    ) : (
                        <>
                            Analyze Code
                            <ArrowRight className="w-5 h-5 ml-2" />
                        </>
                    )}
                </button>
            </div>
        </div>
    );
}
