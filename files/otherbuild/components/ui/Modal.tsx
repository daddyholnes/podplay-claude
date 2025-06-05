import React, { useEffect, useRef, useState } from 'react';
import { XMarkIcon } from '../icons';
import { useTheme } from '../../hooks/useTheme';
import { useDraggable } from '../../hooks/useDraggable'; // Import the hook

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
  size?: 'sm' | 'md' | 'lg' | 'xl' | 'full';
  initialPosition?: { x: number; y: number }; // For draggable
}

const Modal: React.FC<ModalProps> = ({ isOpen, onClose, title, children, size = 'md', initialPosition }) => {
  const { theme } = useTheme();
  const modalContentRef = useRef<HTMLDivElement>(null);
  const modalHeaderRef = useRef<HTMLDivElement>(null); // Handle for dragging

  const [hasBeenDragged, setHasBeenDragged] = useState(false);

  // Setup draggable
  const { currentPosition } = useDraggable({
    contentRef: modalContentRef,
    handleRef: modalHeaderRef, // Draggable by the header
    initialPosition: initialPosition,
    boundsRef: undefined, // No bounds for now, can be added later (e.g., viewportRef)
    onDragStart: () => setHasBeenDragged(true),
  });
  
  // Reset position and dragged state when modal is closed or reopened
  useEffect(() => {
    if (isOpen) {
      setHasBeenDragged(false);
      if (modalContentRef.current) {
        // Reset transform if not using initialPosition or if it should re-center
        if (!initialPosition) {
           modalContentRef.current.style.transform = 'translate(0px, 0px)';
        }
      }
    }
  }, [isOpen, initialPosition]);


  useEffect(() => {
    const handleEsc = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        onClose();
      }
    };
    if (isOpen) {
      document.addEventListener('keydown', handleEsc);
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }
    return () => {
      document.removeEventListener('keydown', handleEsc);
      document.body.style.overflow = 'unset';
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const sizeClasses = {
    sm: 'max-w-sm',
    md: 'max-w-md',
    lg: 'max-w-lg',
    xl: 'max-w-xl',
    full: 'max-w-full w-full h-full rounded-none',
  };
  
  // Dynamic centering: if not dragged, use flex centering. If dragged, rely on transform.
  const centeringClasses = !hasBeenDragged && !initialPosition ? 'items-center justify-center' : '';

  return (
    <div 
      className={`fixed inset-0 z-50 flex ${centeringClasses} bg-black/60 backdrop-blur-sm p-4 animate-fadeIn`}
      // onClick={onClose} // Removed to prevent closing when clicking backdrop if modal is dragged
    >
      <div
        ref={modalContentRef} // Ref for the draggable content
        className={`
          relative ${theme.chatBubbleBg} ${theme.text} rounded-2xl shadow-soft-xl flex flex-col 
          max-h-[90vh] ${sizeClasses[size]} w-full overflow-hidden 
          border ${theme.accent.replace('text-','border-')}/80
          transition-shadow duration-200 ease-in-out 
          ${currentPosition.x !==0 || currentPosition.y !== 0 || hasBeenDragged ? 'absolute' : ''} // Use absolute if dragged to override flex centering
        `}
        style={{ 
           // If initialPosition is provided, modal starts there. Otherwise, centered by flex.
           // Transform is applied by useDraggable. If not using transform in useDraggable, set left/top here.
        }}
        // onClick={(e) => e.stopPropagation()} // Keep this to prevent backdrop click closing if that was re-enabled
      >
        {/* Header acts as the drag handle */}
        <div
          ref={modalHeaderRef} // Ref for the drag handle
          className={`flex items-center justify-between p-4 border-b ${theme.accent.replace('text-','border-')}/30 ${title ? '' : 'py-3'}`}
          style={{ cursor: 'grab' }} // Indicate it's draggable
        >
          {title && <h3 className={`text-lg font-semibold ${theme.accent}`}>{title}</h3>}
          {/* Spacer if no title but still want the close button on the right */}
          {!title && <div className="flex-grow"></div>}
          <button
            onClick={onClose}
            className={`p-1 rounded-full hover:bg-gray-500/20 ${theme.text} ${title ? '' : 'relative z-10'}`}
            aria-label="Close modal"
          >
            <XMarkIcon className="w-6 h-6" />
          </button>
        </div>
        
        <div className="flex-grow overflow-y-auto p-4" style={{ scrollbarWidth: 'thin' }}>{children}</div>
      </div>
    </div>
  );
};

export default Modal;