import { useRef, useEffect, useState, useCallback } from 'react';

interface UseDraggableOptions {
  handleRef: React.RefObject<HTMLElement>; // The element that initiates drag (e.g., modal header)
  contentRef: React.RefObject<HTMLElement>; // The element that moves
  initialPosition?: { x: number; y: number }; // Initial transform translation
  onDragStart?: () => void;
  onDragEnd?: (position: {x: number, y: number}) => void;
  boundsRef?: React.RefObject<HTMLElement>; // Optional: element to constrain dragging within
}

export const useDraggable = ({ 
  handleRef, 
  contentRef, 
  initialPosition, 
  onDragStart, 
  onDragEnd,
  boundsRef 
}: UseDraggableOptions) => {
  const [isDragging, setIsDragging] = useState(false);
  const [position, setPosition] = useState(initialPosition || { x: 0, y: 0 });
  const dragStartOffset = useRef({ x: 0, y: 0 }); // Mouse position relative to element's top-left on drag start

  const onMouseDown = useCallback((e: MouseEvent) => {
    if (handleRef.current && handleRef.current.contains(e.target as Node) && contentRef.current) {
      
      const currentTransform = contentRef.current.style.transform;
      let startX = 0;
      let startY = 0;
      if (currentTransform.includes('translate')) {
          const match = currentTransform.match(/translate\(\s*(-?[\d.]+)px,\s*(-?[\d.]+)px\s*\)/);
          if (match) {
              startX = parseFloat(match[1]);
              startY = parseFloat(match[2]);
          }
      }
      
      dragStartOffset.current = {
        x: e.clientX - startX,
        y: e.clientY - startY,
      };

      setIsDragging(true);
      document.body.style.userSelect = 'none'; // Prevent text selection globally
      document.body.classList.add('grabbing'); // Add grabbing cursor to body
      contentRef.current.style.cursor = 'grabbing';
      if (handleRef.current) handleRef.current.style.cursor = 'grabbing';
      
      if(onDragStart) onDragStart();
      e.preventDefault(); // Prevent default drag behavior (e.g., for images)
    }
  }, [handleRef, contentRef, onDragStart]);

  const onMouseMove = useCallback((e: MouseEvent) => {
    if (!isDragging || !contentRef.current) return;

    let newX = e.clientX - dragStartOffset.current.x;
    let newY = e.clientY - dragStartOffset.current.y;

    if (boundsRef?.current) {
      const parentRect = boundsRef.current.getBoundingClientRect();
      const contentRect = contentRef.current.getBoundingClientRect();
      
      // Assuming contentRef is positioned relative to boundsRef or viewport
      // For transform, newX and newY are the desired translations.
      // We need to check if this new translation would push contentRect outside parentRect.
      
      //Effective top-left of content if it were at newX, newY translation (relative to its offsetParent)
      //This is simplified; assumes transform doesn't affect getBoundingClientRect's left/top much, or that we correct for it.
      //For transform, `left` and `top` from `getBoundingClientRect` are screen coords.
      //The check should be: `parentRect.left` vs `(contentRect.left - currentTranslateX) + newX`

      const currentTranslateX = parseFloat(contentRef.current.style.transform.match(/translate\(\s*(-?[\d.]+)px/)?.[1] || '0');
      const currentTranslateY = parseFloat(contentRef.current.style.transform.match(/translate\([^,]+,\s*(-?[\d.]+)px/)?.[1] || '0');

      const projectedLeft = (contentRect.left - currentTranslateX) + newX;
      const projectedTop = (contentRect.top - currentTranslateY) + newY;

      if (projectedLeft < parentRect.left) {
        newX = currentTranslateX + (parentRect.left - (contentRect.left - currentTranslateX));
      } else if (projectedLeft + contentRect.width > parentRect.right) {
        newX = currentTranslateX + (parentRect.right - contentRect.width - (contentRect.left - currentTranslateX));
      }

      if (projectedTop < parentRect.top) {
        newY = currentTranslateY + (parentRect.top - (contentRect.top - currentTranslateY));
      } else if (projectedTop + contentRect.height > parentRect.bottom) {
         newY = currentTranslateY + (parentRect.bottom - contentRect.height - (contentRect.top - currentTranslateY));
      }
    }
    
    contentRef.current.style.transform = `translate(${newX}px, ${newY}px)`;

  }, [isDragging, contentRef, boundsRef]);

  const onMouseUp = useCallback(() => {
    if (!isDragging || !contentRef.current) return;

    setIsDragging(false);
    document.body.style.userSelect = '';
    document.body.classList.remove('grabbing');
    contentRef.current.style.cursor = '';
    if (handleRef.current) handleRef.current.style.cursor = 'grab'; // Reset to grab

    const finalTransform = contentRef.current.style.transform;
    let finalX = 0;
    let finalY = 0;
     if (finalTransform.includes('translate')) {
        const match = finalTransform.match(/translate\(\s*(-?[\d.]+)px,\s*(-?[\d.]+)px\s*\)/);
        if (match) {
            finalX = parseFloat(match[1]);
            finalY = parseFloat(match[2]);
        }
    }
    setPosition({ x: finalX, y: finalY });
    if (onDragEnd) onDragEnd({ x: finalX, y: finalY });

  }, [isDragging, contentRef, handleRef, onDragEnd]);

  useEffect(() => {
    const handleElement = handleRef.current;
    if (handleElement) {
      handleElement.addEventListener('mousedown', onMouseDown);
      handleElement.style.cursor = 'grab'; // Set initial cursor for handle
    }
    // Listen on document for mousemove and mouseup to allow dragging outside the element
    document.addEventListener('mousemove', onMouseMove);
    document.addEventListener('mouseup', onMouseUp);

    return () => {
      if (handleElement) {
        handleElement.removeEventListener('mousedown', onMouseDown);
        handleElement.style.cursor = '';
      }
      document.removeEventListener('mousemove', onMouseMove);
      document.removeEventListener('mouseup', onMouseUp);
      document.body.style.userSelect = '';
      document.body.classList.remove('grabbing');
      if (contentRef.current) contentRef.current.style.cursor = '';
    };
  }, [handleRef, contentRef, onMouseDown, onMouseMove, onMouseUp]);

  useEffect(() => {
      if (contentRef.current && !isDragging) { // Only apply if not currently dragging to avoid conflict
          contentRef.current.style.transform = `translate(${position.x}px, ${position.y}px)`;
      }
  }, [position, contentRef, isDragging]);
  
  return { currentPosition: position, isDragging };
};
