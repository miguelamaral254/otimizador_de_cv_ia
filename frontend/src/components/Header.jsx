import React from 'react'
import { Link } from 'react-router-dom'

function Header() {
    return (
        <header className="bg-primary-600 text-white p-4">
            <nav className="container mx-auto">
                <ul className="flex space-x-6">
                    <li><Link to="/" className="hover:text-primary-200 transition-colors">Início</Link></li>
                    <li><Link to="/about" className="hover:text-primary-200 transition-colors">Sobre</Link></li>
                    <li><Link to="/contact" className="hover:text-primary-200 transition-colors">Contato</Link></li>
                </ul>
            </nav>
        </header>
    )
}

export default Header
