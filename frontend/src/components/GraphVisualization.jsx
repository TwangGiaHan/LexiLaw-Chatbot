import React, { useEffect, useRef } from 'react';
import cytoscape from 'cytoscape';

// --- CẤU HÌNH PHONG CÁCH CHO ĐỒ THỊ (Styling) ---
// Định nghĩa màu sắc cho từng loại Node
const SCHEMA_STYLING = {
  Document: { color: '#e74c3c', shape: 'diamond', size: 30 },
  Article: { color: '#3498db', shape: 'ellipse', size: 25 },
  Clause: { color: '#8e44ad', shape: 'ellipse', size: 20 },
  Point: { color: '#9b59b6', shape: 'ellipse', size: 15 },
  Span: { color: '#95a5a6', shape: 'ellipse', size: 12 },
  LegalConcept: { color: '#2ecc71', shape: 'triangle', size: 25 },
  Penalty: { color: '#f1c40f', shape: 'star', size: 30 },
  Event: { color: '#e67e22', shape: 'rectangle', size: 25 },
  Actor: { color: '#34495e', shape: 'hexagon', size: 25 },
  Default: { color: '#7f8c8d', shape: 'ellipse', size: 20 },
};

// Định nghĩa màu sắc cho mối quan hệ
const EDGE_COLORS = {
  REFERENCES: '#3498db', // Xanh dương
  DEFINES: '#2ecc71',    // Xanh lá
  HAS_PENALTY: '#f1c40f', // Vàng
  PROHIBITS: '#e74c3c',  // Đỏ
  Default: '#848484'     // Xám
};

// --- CÁC HÀM TIỆN ÍCH (Utilities) ---

// 1. Tạo Nhãn thông minh (Smart Label) cho Node
const generateSmartLabel = (node) => {
  const type = node.type;
  const props = node.properties || {};

  switch (type) {
    case 'Document':
      return props.doc_number || `Luật ${props.doc_key}`;
    case 'Article':
      return `Điều ${props.no}`;
    case 'Clause':
      return `Khoản ${props.no}`;
    case 'Point':
      return `Điểm ${props.no}`;
    case 'LegalConcept':
    case 'Event':
    case 'Actor':
      return props.name || props.name_norm;
    case 'Penalty':
      return props.p_type || `Phạt ${props.amount_max}`;
    case 'Span':
      // Đối với nội dung text, chỉ lấy 20 ký tự đầu
      return props.content ? props.content.substring(0, 20) + '...' : 'Text';
    default:
      return node.label || type;
  }
};

// 2. Tạo nội dung Tooltip (HTML) khi hover
const generateTooltip = (node) => {
  const type = node.type;
  const props = node.properties || {};

  let html = `<b>Type:</b> ${type}<br/><hr/>`;
  Object.entries(props).forEach(([key, value]) => {
    // Không hiển thị các thuộc tính hệ thống
    if (['doc_key', 'article_id', 'clause_id', 'concept_id'].includes(key)) return;

    // Xử lý nội dung dài
    if (typeof value === 'string' && value.length > 200) {
      value = value.substring(0, 200) + '...';
    }

    html += `<b>${key}:</b> ${value}<br/>`;
  });
  return `<div style="max-width:300px; font-size: 12px;">${html}</div>`;
};

const GraphVisualization = ({ graphData }) => {
  const containerRef = useRef(null);
  const cyRef = useRef(null);
  const tooltipRef = useRef(null);

  useEffect(() => {
    if (!graphData || !graphData.nodes || !containerRef.current) return;

    if (cyRef.current) {
      cyRef.current.destroy();
      cyRef.current = null;
    }

    const elements = [
      ...graphData.nodes.map((node) => {
        const type = node.type || 'Default';
        const style = SCHEMA_STYLING[type] || SCHEMA_STYLING.Default;
        const nodeValue = {
          ...node,
          properties: node.properties || {},
        };

        return {
          data: {
            id: String(node.id),
            label: generateSmartLabel(nodeValue),
            type,
            properties: nodeValue.properties,
            _tooltip: generateTooltip(nodeValue),
          },
          position: { x: Math.random() * 400 - 200, y: Math.random() * 400 - 200 },
          style: {
            'background-color': style.color,
            width: style.size + 10,
            height: style.size + 10,
            shape: style.shape,
            color: '#fff',
            'border-color': '#333',
            'border-width': 2,
          }
        };
      }),
      ...graphData.edges.map((edge, idx) => ({
        data: {
          id: edge.id ? String(edge.id) : `edge-${idx}`,
          source: String(edge.source || edge.from),
          target: String(edge.target || edge.to),
          label: edge.label || edge.relationship || '',
          color: EDGE_COLORS[edge.label] || EDGE_COLORS[edge.relationship] || EDGE_COLORS.Default,
        }
      }))
    ];

    cyRef.current = cytoscape({
      container: containerRef.current,
      elements,
      style: [
        {
          selector: 'node',
          style: {
            'label': 'data(label)',
            'text-valign': 'center',
            'text-halign': 'center',
            'font-size': 11,
            'color': '#fff',
            'text-wrap': 'wrap',
            'text-max-width': 80,
            'overlay-padding': 0,
            'overlay-opacity': 0,
            'transition-duration': '400ms',
          }
        },
        {
          selector: 'edge',
          style: {
            'width': 2,
            'line-color': 'data(color)',
            'target-arrow-color': 'data(color)',
            'target-arrow-shape': 'triangle',
            'curve-style': 'bezier',
            'label': 'data(label)',
            'font-size': 9,
            'text-background-color': '#ffffff',
            'text-background-opacity': 0.7,
          }
        }
      ],
      layout: {
        name: 'cose',
        idealEdgeLength: 150,
        nodeOverlap: 30,
        refresh: 20,
        fit: true,
        padding: 20,
        gravity: 0.05,
        numIter: 250,
        initialTemp: 200,
        coolingFactor: 0.95,
      },
    });

    cyRef.current.on('mouseover', 'node', (event) => {
      const node = event.target;
      const tooltip = tooltipRef.current;
      if (!tooltip) return;

      tooltip.innerHTML = node.data('_tooltip');
      tooltip.style.display = 'block';
      tooltip.style.left = `${event.originalEvent.clientX + 12}px`;
      tooltip.style.top = `${event.originalEvent.clientY + 12}px`;
    });

    cyRef.current.on('mouseout', 'node', () => {
      const tooltip = tooltipRef.current;
      if (tooltip) {
        tooltip.style.display = 'none';
      }
    });

    cyRef.current.on('tap', 'node', (event) => {
      const node = event.target;
      console.log('Node pressed:', node.data());
    });

    return () => {
      if (cyRef.current) {
        cyRef.current.destroy();
      }
    };
  }, [graphData]);

  if (!graphData || !graphData.nodes || graphData.nodes.length === 0) {
    return <div className="text-center text-gray-500">Không có dữ liệu đồ thị để hiển thị</div>;
  }

  return (
    <div className="relative w-full h-[75vh] border rounded-lg overflow-hidden">
      <div ref={containerRef} className="w-full h-full" />
      <div ref={tooltipRef} className="vis-tooltip" style={{ display: 'none', position: 'fixed' }} />
    </div>
  );
};

export default GraphVisualization;