'use client'

import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import axios from 'axios'
import { Upload, FileText, Download, Loader2, Award, Clock, CheckCircle2 } from 'lucide-react'

interface ModelOutput {
  flash: string
  pro: string
  lite: string
}

interface AnalysisResult {
  model_outputs: ModelOutput
  raw_outputs: ModelOutput
  scores: { [key: string]: number }
  response_times: { [key: string]: number }
  best_model: string
  model_names: { [key: string]: string }
  errors?: { [key: string]: string }
}

export default function Home() {
  const [file, setFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<AnalysisResult | null>(null)
  const [showRaw, setShowRaw] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [temperature, setTemperature] = useState<number>(0.7)
  const [mediaResolution, setMediaResolution] = useState<'default' | 'high' | 'low'>('default')
  const [thinkingLevel, setThinkingLevel] = useState<'minimal' | 'low' | 'medium' | 'high'>('minimal')

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      setFile(acceptedFiles[0])
      setResult(null)
      setError(null)
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/jpeg': ['.jpg', '.jpeg', '.jfif'],
      'image/png': ['.png'],
      'application/pdf': ['.pdf']
    },
    maxFiles: 1
  })

  const handleAnalyze = async () => {
    if (!file) return

    setLoading(true)
    setError(null)

    const formData = new FormData()
    formData.append('file', file)
    formData.append('temperature', String(temperature))
    formData.append('media_resolution', mediaResolution)
    formData.append('thinking_level', thinkingLevel)

    // 1. Define the base URL using the environment variable
    // Use the Vite one OR the Next.js one, depending on your framework:
    const baseUrl = process.env.NEXT_PUBLIC_API_URL;
    // const baseUrl = process.env.NEXT_PUBLIC_API_URL; 

    try {
      const response = await axios.post<AnalysisResult>(
        // 2. Combine the base URL with your specific endpoint
        `${baseUrl}/api/analyze`, 
        formData,
        {
          headers: { 'Content-Type': 'multipart/form-data' }
        }
      )
      setResult(response.data)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Analysis failed. Please try again.')
    } finally {
      setLoading(false)
    }
}

  const downloadText = (modelKey: string) => {
    if (!result) return
    const text = showRaw ? result.raw_outputs[modelKey as keyof ModelOutput] : result.model_outputs[modelKey as keyof ModelOutput]
    const blob = new Blob([text], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${modelKey}_output.txt`
    a.click()
  }

  const downloadJSON = () => {
    if (!result) return
    const blob = new Blob([JSON.stringify(result, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'analysis_result.json'
    a.click()
  }

  const getScoreColor = (score: number) => {
    if (score >= 0.8) return 'bg-green-500'
    if (score >= 0.6) return 'bg-yellow-500'
    return 'bg-red-500'
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-white mb-4">
            OCR Document Analysis
          </h1>
          <p className="text-xl text-gray-300">
            AI-powered text extraction with multi-model comparison
          </p>
        </div>

        {/* Upload Section */}
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 mb-8 border border-white/20">
          <div
            {...getRootProps()}
            className={`border-3 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all ${
              isDragActive
                ? 'border-purple-400 bg-purple-500/20'
                : 'border-gray-400 hover:border-purple-400 hover:bg-white/5'
            }`}
          >
            <input {...getInputProps()} />
            <Upload className="w-16 h-16 mx-auto mb-4 text-purple-400" />
            {file ? (
              <div>
                <p className="text-white text-lg font-semibold mb-2">{file.name}</p>
                <p className="text-gray-300 text-sm">
                  {(file.size / 1024).toFixed(2)} KB
                </p>
              </div>
            ) : (
              <div>
                <p className="text-white text-lg mb-2">
                  {isDragActive ? 'Drop your file here' : 'Drag & drop your file here'}
                </p>
                <p className="text-gray-400 text-sm">
                  Supports JPG, PNG, and PDF files
                </p>
              </div>
            )}
          </div>

          {file && (
            <>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6 text-white">
                <div className="flex flex-col gap-2 bg-white/5 rounded-lg p-4 border border-white/10">
                  <label className="text-sm text-gray-200">Temperature ({temperature.toFixed(1)})</label>
                  <input
                    type="range"
                    min={0}
                    max={1}
                    step={0.1}
                    value={temperature}
                    onChange={(e) => setTemperature(parseFloat(e.target.value))}
                    className="w-full accent-purple-500"
                  />
                </div>

                <div className="flex flex-col gap-2 bg-white/5 rounded-lg p-4 border border-white/10">
                  <label className="text-sm text-gray-200">Media resolution</label>
                  <select
                    value={mediaResolution}
                    onChange={(e) => setMediaResolution(e.target.value as 'default' | 'high' | 'low')}
                    className="bg-slate-900 border border-white/10 rounded-md px-3 py-2 text-white"
                  >
                    <option value="default">Default</option>
                    <option value="high">High</option>
                    <option value="low">Low</option>
                  </select>
                </div>

                <div className="flex flex-col gap-2 bg-white/5 rounded-lg p-4 border border-white/10">
                  <label className="text-sm text-gray-200">Thinking level</label>
                  <select
                    value={thinkingLevel}
                    onChange={(e) => setThinkingLevel(e.target.value as 'minimal' | 'low' | 'medium' | 'high')}
                    className="bg-slate-900 border border-white/10 rounded-md px-3 py-2 text-white"
                  >
                    <option value="minimal">Minimal</option>
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                  </select>
                </div>
              </div>

              <button
                onClick={handleAnalyze}
                disabled={loading}
                className="w-full mt-6 bg-gradient-to-r from-purple-600 to-pink-600 text-white py-4 rounded-xl font-semibold text-lg hover:from-purple-700 hover:to-pink-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-3"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-6 h-6 animate-spin" />
                    Analyzing with 3 AI models...
                  </>
                ) : (
                  <>
                    <FileText className="w-6 h-6" />
                    Analyze Document
                  </>
                )}
              </button>
            </>
          )}

          {error && (
            <div className="mt-4 p-4 bg-red-500/20 border border-red-500 rounded-lg text-red-200">
              {error}
            </div>
          )}
        </div>

        {/* Results Section */}
        {result && (
          <div className="space-y-6">
            {/* Controls */}
            <div className="flex justify-between items-center bg-white/10 backdrop-blur-lg rounded-xl p-4 border border-white/20">
              <div className="flex gap-4">
                <button
                  onClick={() => setShowRaw(!showRaw)}
                  className="px-6 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-all"
                >
                  {showRaw ? 'Show Cleaned' : 'Show Raw'}
                </button>
                <button
                  onClick={downloadJSON}
                  className="px-6 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-all flex items-center gap-2"
                >
                  <Download className="w-4 h-4" />
                  Download JSON
                </button>
              </div>
              <div className="flex items-center gap-2 text-white">
                <Award className="w-5 h-5 text-yellow-400" />
                <span className="font-semibold">Best Model:</span>
                <span className="text-yellow-400">{result.best_model}</span>
              </div>
            </div>

            {/* Model Outputs Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {(['flash', 'pro', 'lite'] as const).map((modelKey) => (
                <div
                  key={modelKey}
                  className={`bg-white/10 backdrop-blur-lg rounded-xl border-2 overflow-hidden ${
                    result.model_names[modelKey] === result.best_model
                      ? 'border-yellow-400 shadow-lg shadow-yellow-400/50'
                      : 'border-white/20'
                  }`}
                >
                  {/* Model Header */}
                  <div className="bg-gradient-to-r from-purple-600 to-pink-600 p-4">
                    <div className="flex items-center justify-between mb-3">
                      <h3 className="text-white font-bold text-lg">
                        {result.model_names[modelKey]}
                      </h3>
                      {result.model_names[modelKey] === result.best_model && (
                        <CheckCircle2 className="w-6 h-6 text-yellow-400" />
                      )}
                    </div>

                    {/* Score Bar */}
                    <div className="mb-2">
                      <div className="flex justify-between text-white text-sm mb-1">
                        <span>Score</span>
                        <span className="font-bold">{(result.scores[modelKey] * 100).toFixed(0)}%</span>
                      </div>
                      <div className="w-full bg-white/20 rounded-full h-3 overflow-hidden">
                        <div
                          className={`h-full ${getScoreColor(result.scores[modelKey])} transition-all duration-500`}
                          style={{ width: `${result.scores[modelKey] * 100}%` }}
                        />
                      </div>
                    </div>

                    {/* Response Time */}
                    <div className="flex items-center gap-2 text-white text-sm">
                      <Clock className="w-4 h-4" />
                      <span>{result.response_times[modelKey]}s</span>
                    </div>
                  </div>

                  {/* Output Text */}
                  <div className="p-4">
                    {result.errors?.[modelKey] && (
                      <div className="mb-3 p-3 rounded-md bg-red-500/20 border border-red-500 text-red-100 text-sm">
                        Model error: {result.errors[modelKey]}
                      </div>
                    )}
                    <div className="bg-slate-900/50 rounded-lg p-4 max-h-96 overflow-y-auto">
                      <pre className="text-gray-200 text-sm whitespace-pre-wrap font-mono">
                        {showRaw
                          ? result.raw_outputs[modelKey] || 'No output'
                          : result.model_outputs[modelKey] || 'No output'}
                      </pre>
                    </div>
                    <button
                      onClick={() => downloadText(modelKey)}
                      className="w-full mt-3 px-4 py-2 bg-white/10 hover:bg-white/20 text-white rounded-lg transition-all flex items-center justify-center gap-2"
                    >
                      <Download className="w-4 h-4" />
                      Download Text
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </main>
  )
}
