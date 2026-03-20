const relationGraphState = {
    selectedFamily: "all",
    selectedRelation: "all",
    focusedNodeId: null,
    viewportWidth: 960,
    viewportHeight: 600,
    nodeSelection: null,
    linkSelection: null,
    nodesData: [],
    linksData: [],
    nodeMap: new Map(),
    svgSelection: null,
    zoomBehavior: null,
  };
  
  function initRelationGraph() {
    const container = document.getElementById("relation-canvas");
    if (!container) return;
    if (typeof d3 === "undefined") {
      renderGraphStatus("关系图加载失败：D3.js 未加载，请检查网络或 CDN 访问。");
      return;
    }
  
    try {
      const width = container.clientWidth || 960;
      const height = 600;
      // 使用合并后的数据
      const nodes = graphNodes.map((d) => ({ ...d }));
      const links = graphLinks.map((d) => ({ ...d }));
      const nodeMap = new Map(nodes.map((n) => [n.id, n]));
  
      d3.select(container).selectAll("*").remove();
  
      const svg = d3
        .select(container)
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", `0 0 ${width} ${height}`);
  
      const graphLayer = svg.append("g").attr("class", "graph-layer");
  
      svg.on("click", (event) => {
        const clickedNode = event.target.closest(".relation-node");
        if (!clickedNode) {
          clearNodeFocus();
        }
      });
  
      const zoomBehavior = d3
        .zoom()
        .scaleExtent([0.4, 2.5])
        .on("zoom", (event) => graphLayer.attr("transform", event.transform));
      svg.call(zoomBehavior);
  
      const link = graphLayer
        .append("g")
        .attr("class", "links")
        .selectAll("line")
        .data(links)
        .enter()
        .append("line")
        .attr("class", (d) => `relation-line ${d.type}-line`)
        .attr("stroke", (d) => getLineColor(d.type))
        .attr("stroke-width", (d) => (d.type === "marriage" || d.type === "love" ? 2.5 : 2))
        .attr("stroke-dasharray", (d) => (d.type === "family" ? "5,5" : "0"));
  
      const node = graphLayer
        .append("g")
        .attr("class", "nodes")
        .selectAll("g")
        .data(nodes)
        .enter()
        .append("g")
        .attr("class", "relation-node")
        .style("cursor", "pointer")
        .call(
          d3
            .drag()
            .on("start", dragStart)
            .on("drag", dragging)
            .on("end", dragEnd)
        )
        .on("click", (event, d) => {
          event.stopPropagation();
          focusCharacterNode(d.id);
          if (d.type === "plot") {
            // 情节节点：显示情节卡牌
            const plotNameEl = document.getElementById("plotName");
            const plotDescEl = document.getElementById("plotDesc");
            const plotCharactersEl = document.getElementById("plotCharacters");
            const plotModalEl = document.getElementById("plotCardModal");
            if (plotNameEl && plotDescEl && plotCharactersEl && plotModalEl && typeof bootstrap !== "undefined") {
              plotNameEl.textContent = d.name;
              plotDescEl.textContent = d.desc || "暂无描述";
              const involved = getPlotInvolvedCharacters(d.id);
              if (involved.length > 0) {
                plotCharactersEl.innerHTML = involved
                  .map(
                    (item) =>
                      `<li class="plot-character-item clickable" data-character-id="${item.id}" role="button" tabindex="0">${item.name}</li>`
                  )
                  .join("");
              } else {
                plotCharactersEl.innerHTML = '<li class="plot-character-item">暂无</li>';
              }
              const plotModal = new bootstrap.Modal(plotModalEl);
              plotModal.show();
              bindPlotCharacterJumpEvents();
            }
          } else {
            // 人物节点：调用原有人物卡片函数
            if (typeof showCharacterCard === "function") {
              showCharacterCard(d.id);
            }
          }
        });
  
      // 绘制节点形状（圆形/菱形）和文字
      node.each(function(d) {
        const group = d3.select(this);
        // 清除可能残留的内容
        group.selectAll("*").remove();

        if (d.type === "plot") {
          // 情节节点：菱形（旋转45度的正方形）
          group.append("rect")
            .attr("width", 30)
            .attr("height", 30)
            .attr("x", -15)
            .attr("y", -15)
            .attr("transform", "rotate(45)")
            .attr("fill", "#DAA520")      // 金色
            .attr("stroke", "#8B4513")
            .attr("stroke-width", 2)
            .attr("rx", 4);               // 轻微圆角
        } else {
          // 人物节点：带图片的圆形
          const radius = getNodeRadius(d.type);
          
          // 添加圆形背景
          group.append("circle")
            .attr("r", radius)
            .attr("fill", getGroupColor(d.group))
            .attr("stroke", d.type === "main" ? "#DC143C" : "#8B4513")
            .attr("stroke-width", d.type === "main" ? 2.5 : 2)
            .attr("opacity", 0.95);
          
          // 添加人物图片
          if (d.image) {
            const clipId = "clip-" + d.id;
            
            // 创建裁剪路径（圆形）
            group.append("defs")
              .append("clipPath")
              .attr("id", clipId)
              .append("circle")
              .attr("r", radius - 3);
            
            // 添加图片
            group.append("image")
              .attr("href", d.image)
              .attr("x", -radius + 3)
              .attr("y", -radius + 3)
              .attr("width", (radius - 3) * 2)
              .attr("height", (radius - 3) * 2)
              .attr("clip-path", "url(#" + clipId + ")")
              .attr("preserveAspectRatio", "xMidYMid slice");
          }
        }

        // 添加文字
        group.append("text")
          .text(d.name)
          .attr("dy", d.type === "plot" ? 35 : getNodeRadius(d.type) + 16)
          .attr("text-anchor", "middle")
          .attr("font-family", "'Noto Serif SC', serif")
          .attr("font-size", "12px")
          .attr("fill", "#5D3A1A");
      });
  
      const simulation = d3
        .forceSimulation(nodes)
        .force(
          "link",
          d3
            .forceLink(links)
            .id((d) => d.id)
            .distance((d) => getLinkDistance(d.type))
            .strength(0.5)
        )
        .force("charge", d3.forceManyBody().strength(-420))
        .force("center", d3.forceCenter(width / 2, height / 2))
        .force("collision", d3.forceCollide().radius((d) => {
          if (d.type === "plot") return 25;
          return getNodeRadius(d.type) + 18;
        }))
        .on("tick", () => {
          link
            .attr("x1", (d) => d.source.x)
            .attr("y1", (d) => d.source.y)
            .attr("x2", (d) => d.target.x)
            .attr("y2", (d) => d.target.y);
          node.attr("transform", (d) => `translate(${d.x},${d.y})`);
        });
  
      function dragStart(event, d) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
      }
  
      function dragging(event, d) {
        d.fx = event.x;
        d.fy = event.y;
      }
  
      function dragEnd(event, d) {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
      }
  
      relationGraphState.nodeSelection = node;
      relationGraphState.linkSelection = link;
      relationGraphState.nodesData = nodes;
      relationGraphState.linksData = links;
      relationGraphState.nodeMap = nodeMap;
      relationGraphState.viewportWidth = width;
      relationGraphState.viewportHeight = height;
      relationGraphState.svgSelection = svg;
      relationGraphState.zoomBehavior = zoomBehavior;
  
      bindFamilyFilterEvents();
      bindRelationFilterEvents();
      applyGraphFilters();
    } catch (error) {
      renderGraphStatus(`关系图渲染失败：${error.message}`);
      console.error("initRelationGraph error:", error);
    }
  }
  
  function bindFamilyFilterEvents() {
    const panel = document.getElementById("familyFilterPanel");
    if (!panel || panel.dataset.bound === "1") return;
  
    panel.addEventListener("click", (event) => {
      const btn = event.target.closest("[data-family-filter]");
      if (!btn) return;
      relationGraphState.selectedFamily = btn.dataset.familyFilter || "all";
      applyGraphFilters();
    });
  
    panel.dataset.bound = "1";
  }
  
  function bindRelationFilterEvents() {
    const panel = document.getElementById("relationTypePanel");
    if (!panel || panel.dataset.bound === "1") return;
  
    panel.addEventListener("click", (event) => {
      const btn = event.target.closest("[data-relation-filter]");
      if (!btn) return;
      relationGraphState.selectedRelation = btn.dataset.relationFilter || "all";
      applyGraphFilters();
    });
  
    panel.dataset.bound = "1";
  }
  
  function applyGraphFilters() {
    const { nodeSelection, linkSelection, nodeMap, selectedFamily, selectedRelation, focusedNodeId, linksData } = relationGraphState;
    if (!nodeSelection || !linkSelection) return;
  
    // 更新按钮激活状态
    document.querySelectorAll("[data-family-filter]").forEach((btn) => {
      btn.classList.toggle("active", btn.dataset.familyFilter === selectedFamily);
    });
    document.querySelectorAll("[data-relation-filter]").forEach((btn) => {
      btn.classList.toggle("active", btn.dataset.relationFilter === selectedRelation);
    });
  
    const focusedNeighbors = new Set();
    if (focusedNodeId) {
      focusedNeighbors.add(focusedNodeId);
      linksData.forEach((l) => {
        const sourceId = getEndpointId(l.source);
        const targetId = getEndpointId(l.target);
        if (sourceId === focusedNodeId) focusedNeighbors.add(targetId);
        if (targetId === focusedNodeId) focusedNeighbors.add(sourceId);
      });
    }
  
    // 节点过滤：情节节点在家族筛选时可见，但人物聚焦时仍遵循一度关系
    const nodePasses = (d) => {
      if (d.type === "plot") {
        const focusPass = !focusedNodeId || focusedNeighbors.has(d.id);
        return focusPass;
      }
      const familyPass = selectedFamily === "all" || d.group === selectedFamily;
      const focusPass = !focusedNodeId || focusedNeighbors.has(d.id);
      return familyPass && focusPass;
    };
  
    nodeSelection.style("opacity", (d) => (nodePasses(d) ? 1 : 0.16));
  
    // 连线过滤
    linkSelection
      .style("opacity", (d) => {
        const sourceId = getEndpointId(d.source);
        const targetId = getEndpointId(d.target);
        const sourceNode = nodeMap.get(sourceId);
        const targetNode = nodeMap.get(targetId);
        const typePass = selectedRelation === "all" || d.type === selectedRelation;
        // 家族过滤：如果任一端是情节节点，则连线始终显示（只要类型和焦点通过）
        const familyPass =
          selectedFamily === "all" ||
          sourceNode?.type === "plot" ||
          targetNode?.type === "plot" ||
          sourceNode?.group === selectedFamily ||
          targetNode?.group === selectedFamily;
        const focusPass =
          !focusedNodeId || sourceId === focusedNodeId || targetId === focusedNodeId;
        return typePass && familyPass && focusPass ? 0.95 : 0.07;
      })
      .attr("stroke-width", (d) => {
        const typePass = selectedRelation === "all" || d.type === selectedRelation;
        const sourceId = getEndpointId(d.source);
        const targetId = getEndpointId(d.target);
        const focusPass =
          !focusedNodeId || sourceId === focusedNodeId || targetId === focusedNodeId;
        if (typePass && focusPass) {
          return d.type === "marriage" || d.type === "love" ? 3 : 2.6;
        }
        return 1.2;
      });
  }
  
  function focusCharacterNode(characterId) {
    relationGraphState.focusedNodeId = characterId || null;
    applyGraphFilters();
  }
  
  function clearNodeFocus() {
    relationGraphState.focusedNodeId = null;
    applyGraphFilters();
  }
  
  function getEndpointId(endpoint) {
    if (endpoint && typeof endpoint === "object") return endpoint.id;
    return endpoint;
  }

  function getPlotInvolvedCharacters(plotId) {
    const { linksData, nodeMap } = relationGraphState;
    const people = new Map();

    linksData.forEach((l) => {
      const sourceId = getEndpointId(l.source);
      const targetId = getEndpointId(l.target);
      if (sourceId !== plotId && targetId !== plotId) return;

      const otherId = sourceId === plotId ? targetId : sourceId;
      const otherNode = nodeMap.get(otherId);
      if (!otherNode || otherNode.type === "plot") return;
      people.set(otherNode.id, { id: otherNode.id, name: otherNode.name });
    });

    return Array.from(people.values());
  }

  function bindPlotCharacterJumpEvents() {
    const listEl = document.getElementById("plotCharacters");
    const plotModalEl = document.getElementById("plotCardModal");
    if (!listEl || !plotModalEl || listEl.dataset.bound === "1") return;

    const jumpToCharacter = (target) => {
      const characterId = target?.dataset?.characterId;
      if (!characterId) return;

      focusCharacterNode(characterId);
      focusNodeWithZoom(characterId);

      if (typeof bootstrap !== "undefined") {
        const modalInstance = bootstrap.Modal.getInstance(plotModalEl);
        if (modalInstance) modalInstance.hide();
      }

      if (typeof showCharacterCard === "function") {
        showCharacterCard(characterId);
      }
    };

    listEl.addEventListener("click", (event) => {
      const target = event.target.closest(".plot-character-item.clickable");
      if (!target) return;
      jumpToCharacter(target);
    });

    listEl.addEventListener("keydown", (event) => {
      if (event.key !== "Enter" && event.key !== " ") return;
      const target = event.target.closest(".plot-character-item.clickable");
      if (!target) return;
      event.preventDefault();
      jumpToCharacter(target);
    });

    listEl.dataset.bound = "1";
  }

  function focusNodeWithZoom(characterId) {
    const { nodeMap, svgSelection, zoomBehavior, viewportWidth, viewportHeight } = relationGraphState;
    if (!svgSelection || !zoomBehavior) return;

    const targetNode = nodeMap.get(characterId);
    if (!targetNode || typeof targetNode.x !== "number" || typeof targetNode.y !== "number") return;

    const scale = 1.35;
    const transform = d3.zoomIdentity
      .translate(viewportWidth / 2 - targetNode.x * scale, viewportHeight / 2 - targetNode.y * scale)
      .scale(scale);

    svgSelection
      .transition()
      .duration(450)
      .ease(d3.easeCubicOut)
      .call(zoomBehavior.transform, transform);
  }
  
  function renderGraphStatus(message) {
    const container = document.getElementById("relation-canvas");
    if (!container) return;
    container.innerHTML = `<div style="height:100%;display:flex;align-items:center;justify-content:center;color:#8B4513;font-family:'Noto Serif SC',serif;padding:16px;text-align:center;">${message}</div>`;
  }
  
  // 导出函数供外部调用
  window.focusCharacterInGraph = focusCharacterNode;
  window.clearCharacterFocusInGraph = clearNodeFocus;
  window.initRelationGraph = initRelationGraph;
  
  // 颜色辅助函数
  function getLineColor(type) {
    switch (type) {
      case "love":
        return "#DC143C";
      case "marriage":
        return "#8B4513";
      case "family":
        return "#D2B48C";
      case "servant":
        return "#6B8E23";
      case "friend":
        return "#4169E1";
      case "rival":
        return "#9932CC";
      case "involved":
        return "#1E88E5"; // 情节关联（与 CSS 图例一致）
      default:
        return "#999";
    }
  }
  
  function getGroupColor(group) {
    switch (group) {
      case "贾":
        return "#B22222";
      case "林":
        return "#228B22";
      case "薛":
        return "#DAA520";
      case "王":
        return "#4682B4";
      case "史":
        return "#DA70D6";
      case "丫鬟":
        return "#708090";
      default:
        return "#A9A9A9";
    }
  }
  
  function getNodeRadius(type) {
    if (type === "main") return 28;
    if (type === "servant") return 20;
    return 24; // 普通人物
  }
  
  function getLinkDistance(type) {
    switch (type) {
      case "servant":
        return 110;
      case "marriage":
        return 150;
      case "love":
        return 160;
      case "family":
        return 170;
      case "involved":
        return 150;
      default:
        return 180;
    }
  }
  
  window.addEventListener("load", initRelationGraph);
  window.addEventListener("resize", () => {
    clearTimeout(window.__relationGraphResizeTimer);
    window.__relationGraphResizeTimer = setTimeout(initRelationGraph, 150);
  });