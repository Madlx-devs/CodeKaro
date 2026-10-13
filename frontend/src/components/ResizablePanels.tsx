import React, { useCallback, useEffect, useRef, useState } from 'react';

interface Props {
  left: React.ReactNode;
  center: React.ReactNode;
  right: React.ReactNode;
}

const STORAGE_KEY = 'dsa_panel_widths';

/**
 * Three resizable panels with two draggable dividers (desktop).
 * On narrow screens the panels stack vertically via CSS.
 */
export function ResizablePanels({ left, center, right }: Props) {
  const [widths, setWidths] = useState<[number, number, number]>(() => {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        const parsed = JSON.parse(raw) as [number, number, number];
        if (parsed.length === 3 && parsed.every((n) => n >= 10 && n <= 70)) return parsed;
      }
    } catch {
      // fall through to defaults
    }
    return [27, 43, 30];
  });
  const drag = useRef<{ index: number; startX: number; start: [number, number, number] } | null>(
    null,
  );

  const onMouseMove = useCallback((e: MouseEvent) => {
    if (!drag.current) return;
    const { index, startX, start } = drag.current;
    const grid = document.querySelector<HTMLElement>('.panels');
    if (!grid) return;
    const totalPx = grid.getBoundingClientRect().width;
    if (totalPx <= 0) return;
    const deltaPct = ((e.clientX - startX) / totalPx) * 100;
    const next: [number, number, number] = [...start] as [number, number, number];
    next[index] = Math.min(60, Math.max(15, start[index] + deltaPct));
    next[index + 1] = Math.min(60, Math.max(15, start[index + 1] - deltaPct));
    setWidths(next);
  }, []);

  const onMouseUp = useCallback(() => {
    if (drag.current) {
      drag.current = null;
      document.body.style.cursor = '';
      setWidths((w) => {
        try {
          localStorage.setItem(STORAGE_KEY, JSON.stringify(w));
        } catch {
          // ignore
        }
        return w;
      });
    }
  }, []);

  useEffect(() => {
    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);
    return () => {
      window.removeEventListener('mousemove', onMouseMove);
      window.removeEventListener('mouseup', onMouseUp);
    };
  }, [onMouseMove, onMouseUp]);

  const startDrag = (index: number) => (e: React.MouseEvent) => {
    e.preventDefault();
    drag.current = { index, startX: e.clientX, start: [...widths] as [number, number, number] };
    document.body.style.cursor = 'col-resize';
  };

  return (
    <div
      className="panels"
      style={{
        gridTemplateColumns: `${widths[0]}% 8px ${widths[1]}% 8px ${widths[2]}%`,
      }}
    >
      <section className="panel panel-left" aria-label="Problem details">
        {left}
      </section>
      <div
        className="divider"
        role="separator"
        aria-orientation="vertical"
        aria-label="Resize left panel"
        onMouseDown={startDrag(0)}
      />
      <section className="panel panel-center" aria-label="Code editor">
        {center}
      </section>
      <div
        className="divider"
        role="separator"
        aria-orientation="vertical"
        aria-label="Resize right panel"
        onMouseDown={startDrag(1)}
      />
      <section className="panel panel-right" aria-label="Tests and results">
        {right}
      </section>
    </div>
  );
}
