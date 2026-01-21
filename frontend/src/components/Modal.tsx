import { XMarkIcon } from '@heroicons/react/24/outline'
import { useEffect } from 'react'

interface ModalProps {
  isOpen: boolean
  onClose: () => void
  title: string
  children: React.ReactNode
}

export default function Modal({ isOpen, onClose, title, children }: ModalProps) {
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden'
    } else {
      document.body.style.overflow = 'unset'
    }
    return () => {
      document.body.style.overflow = 'unset'
    }
  }, [isOpen])

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto fade-in">
      <div className="flex min-h-screen items-center justify-center p-4">
        {/* Backdrop with blur effect */}
        <div
          className="fixed inset-0 bg-black/60 backdrop-blur-md transition-opacity"
          onClick={onClose}
        />

        {/* Modal with enhanced styling */}
        <div className="relative bg-white rounded-3xl shadow-2xl max-w-2xl w-full p-8 z-10 transform transition-all slide-in border-2 border-neutral-100">
          {/* Header with gradient */}
          <div className="flex items-center justify-between mb-6 pb-4 border-b-2 border-gradient-to-r from-primary/20 to-transparent">
            <h2 className="text-2xl font-bold gradient-text flex items-center">
              <div className="w-2 h-8 bg-gradient-to-b from-primary to-accent rounded-full mr-3"></div>
              {title}
            </h2>
            <button
              onClick={onClose}
              className="text-neutral-400 hover:text-accent hover:rotate-90 transition-all duration-300 hover:scale-110"
            >
              <XMarkIcon className="w-7 h-7" />
            </button>
          </div>

          {/* Content */}
          <div className="max-h-[70vh] overflow-y-auto custom-scrollbar">
            {children}
          </div>
        </div>
      </div>
    </div>
  )
}
