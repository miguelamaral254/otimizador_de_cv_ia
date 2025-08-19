import React from 'react'

function Home() {
    return (
        <div className="container mx-auto px-4 py-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-6">
                Bem-vindo ao Otimizador de Currículos com IA
            </h1>
            <p className="text-lg text-gray-600 mb-8">
                Esta é a página inicial do projeto. Aqui você pode começar a implementar as funcionalidades do sistema.
            </p>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="card">
                    <h3 className="text-xl font-semibold text-gray-900 mb-3">Upload de CV</h3>
                    <p className="text-gray-600">
                        Implemente o sistema de upload de currículos em PDF.
                    </p>
                </div>

                <div className="card">
                    <h3 className="text-xl font-semibold text-gray-900 mb-3">Análise com IA</h3>
                    <p className="text-gray-600">
                        Integre APIs de IA para análise de currículos.
                    </p>
                </div>

                <div className="card">
                    <h3 className="text-xl font-semibold text-gray-900 mb-3">Dashboard</h3>
                    <p className="text-gray-600">
                        Crie um dashboard para visualizar métricas e progresso.
                    </p>
                </div>
            </div>
        </div>
    )
}

export default Home
