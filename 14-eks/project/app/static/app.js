"use strict";

/* ---------- Small helpers ---------- */
const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];

// Build DOM nodes with textContent only, so cluster data can never inject markup.
function el(tag, props = {}, ...kids) {
    const node = document.createElement(tag);
    for (const [key, value] of Object.entries(props)) {
        if (value === undefined || value === null || value === false) continue;
        if (key === "class") node.className = value;
        else if (key === "text") node.textContent = value;
        else node.setAttribute(key, value);
    }
    node.append(...kids.flat().filter((kid) => kid !== null && kid !== undefined));
    return node;
}

function duration(total) {
    if (total === null || total === undefined) return "-";
    const seconds = Math.floor(total);
    if (seconds < 60) return `${seconds}s`;
    const minutes = Math.floor(seconds / 60);
    if (minutes < 60) return `${minutes}m`;
    const hours = Math.floor(minutes / 60);
    if (hours < 24) return `${hours}h ${minutes % 60}m`;
    return `${Math.floor(hours / 24)}d ${hours % 24}h`;
}

function bytes(value) {
    if (value === null || value === undefined) return "-";
    const mib = value / 1048576;
    return mib >= 1024 ? `${(mib / 1024).toFixed(1)} GiB` : `${Math.round(mib)} MiB`;
}

function statusClass(status) {
    if (["Running", "Succeeded", "Completed"].includes(status)) return "ok";
    if (["Pending", "ContainerCreating", "PodInitializing", "Terminating"].includes(status)) return "warn";
    return "bad";
}

const clock = () => new Date().toLocaleTimeString([], { hour12: false });

/* ---------- State ---------- */
let data = null;
let live = true;
let timer = null;
let selectedPod = null;
let topologySignature = "";
const seen = new Set();

/* ---------- Routing between the four views ---------- */
const views = ["overview", "pods", "events", "deploy"];

function route() {
    const wanted = location.hash.slice(1);
    const view = views.includes(wanted) ? wanted : "overview";

    views.forEach((name) => {
        $(`#view-${name}`).hidden = name !== view;
    });

    $$(".nav").forEach((link) => {
        if (link.dataset.view === view) link.setAttribute("aria-current", "page");
        else link.removeAttribute("aria-current");
    });
}

window.addEventListener("hashchange", route);

/* ---------- Rendering ---------- */
function renderBar() {
    const { cluster, mode } = data;
    $("#clusterName").textContent = cluster.name;
    $("#clusterMeta").textContent = `Kubernetes ${cluster.version} in ${cluster.region}, ${cluster.environment}`;

    const pill = $("#modePill");
    pill.textContent = mode === "cluster" ? "Live cluster data" : "Sample data";
    pill.className = `pill ${mode === "cluster" ? "live" : "demo"}`;

    const banner = $("#banner");
    banner.hidden = mode === "cluster";
    banner.textContent = data.reason || "";
}

function renderSeen() {
    const list = $("#seenList");
    list.replaceChildren(...[...seen].map((name) => el("code", { text: name })));
}

function renderHero() {
    const me = data.me;
    const cut = me.pod.lastIndexOf("-");
    $("#heroPrefix").textContent = cut > 0 ? me.pod.slice(0, cut + 1) : "";
    $("#heroSuffix").textContent = cut > 0 ? me.pod.slice(cut + 1) : me.pod;

    $("#heroNode").textContent = me.node;
    $("#heroIp").textContent = me.pod_ip;
    $("#heroUptime").textContent = duration(me.uptime_seconds);
    $("#heroReq").textContent = me.requests_served.toLocaleString();

    seen.add(me.pod);
    renderSeen();
}

function setRing(svg, percent) {
    const circumference = 2 * Math.PI * 44;
    const value = $(".val", svg);
    const clamped = Math.min(100, Math.max(0, percent || 0));
    value.style.strokeDasharray = circumference;
    value.style.strokeDashoffset = circumference * (1 - clamped / 100);
}

function renderGauges() {
    const m = data.metrics;

    setRing($("#ringCpu"), m.cpu_percent);
    $("#cpuText").textContent = `${Math.round(m.cpu_percent)}%`;
    $("#cpuNote").textContent = `of ${m.cpu_cores} core${m.cpu_cores === 1 ? "" : "s"}`;

    setRing($("#ringMem"), m.memory_percent);
    $("#memText").textContent = m.memory_percent === null ? "-" : `${Math.round(m.memory_percent)}%`;
    $("#memNote").textContent = `${bytes(m.memory_bytes)} of ${bytes(m.memory_limit_bytes)}`;
}

function renderBand() {
    const c = data.counts;
    $("#bNodes").textContent = `${c.nodes_ready}/${c.nodes}`;
    $("#bPods").textContent = `${c.pods_running}/${c.pods}`;
    $("#bReplicas").textContent = `${c.replicas_ready}/${c.replicas_desired}`;
    $("#bReplicasSub").textContent = `Across ${c.deployments} deployment${c.deployments === 1 ? "" : "s"}`;
    $("#bServices").textContent = c.services;
}

function renderTopology() {
    // Rebuilding the tiles would drop keyboard focus, so only do it when something changed.
    const signature = JSON.stringify([
        data.me.pod,
        selectedPod,
        data.topology.map((n) => [n.name, n.ready, n.virtual, n.pods.map((p) => [p.name, p.status])]),
    ]);
    if (signature === topologySignature) return;
    topologySignature = signature;

    const container = $("#topology");

    if (!data.topology.length) {
        container.replaceChildren(el("p", { class: "empty", text: "No nodes were found." }));
        return;
    }

    container.replaceChildren(
        ...data.topology.map((node) =>
            el("div", { class: "node" },
                el("div", { class: "node-head" },
                    el("div", {},
                        el("p", { class: "node-name", text: node.virtual ? "Not scheduled yet" : node.name }),
                        el("p", {
                            class: "node-meta",
                            text: node.virtual ? "These pods are waiting for a node" : `${node.instance_type} in ${node.zone}`,
                        }),
                    ),
                    node.virtual
                        ? null
                        : el("span", {
                            class: `node-state st ${node.ready ? "ok" : "bad"}`,
                            text: node.ready ? "Ready" : "Not ready",
                        }),
                ),
                node.pods.length
                    ? el("div", { class: "tiles" }, ...node.pods.map(renderTile))
                    : el("p", { class: "empty", text: "No pods from this app are on this node." }),
            ),
        ),
    );
}

function renderTile(pod) {
    const isYou = pod.name === data.me.pod;
    const suffix = pod.name.slice(pod.name.lastIndexOf("-") + 1);

    const tile = el("button", {
        type: "button",
        class: `tile ${statusClass(pod.status)}${isYou ? " you" : ""}`,
        title: pod.name,
        "aria-pressed": String(pod.name === selectedPod),
        "aria-label": `${pod.name}, ${pod.status}${isYou ? ", the pod answering this page" : ""}`,
    },
        isYou ? el("span", { class: "you-tag", text: "you" }) : null,
        el("span", { class: "tile-id", text: suffix }),
        el("span", { class: "tile-state", text: pod.status }),
    );

    tile.addEventListener("click", () => {
        selectedPod = selectedPod === pod.name ? null : pod.name;
        renderTopology();
        renderPodInfo();
    });

    return tile;
}

function renderPodInfo() {
    const box = $("#podInfo");
    const pod = data.pods.find((p) => p.name === selectedPod);

    if (!pod) {
        selectedPod = null;
        box.replaceChildren(document.createTextNode("Select a pod to see its details."));
        return;
    }

    const fact = (label, value) => el("div", {}, el("dt", { text: label }), el("dd", { text: value }));

    box.replaceChildren(
        el("dl", {},
            fact("Name", pod.name),
            fact("Status", pod.status),
            fact("Ready", pod.ready),
            fact("Restarts", String(pod.restarts)),
            fact("IP", pod.ip),
            fact("Age", duration(pod.age_seconds)),
        ),
    );
}

function renderPods() {
    const query = $("#podFilter").value.trim().toLowerCase();
    const rows = data.pods.filter((pod) =>
        [pod.name, pod.node, pod.ip, pod.status].some((value) => value.toLowerCase().includes(query)),
    );

    $("#podCount").textContent = `${rows.length} of ${data.pods.length} pods`;

    $("#podRows").replaceChildren(
        ...(rows.length
            ? rows.map((pod) =>
                el("tr", {},
                    el("td", { class: "mono", text: pod.name }),
                    el("td", {}, el("span", { class: `st ${statusClass(pod.status)}`, text: pod.status })),
                    el("td", { text: pod.ready }),
                    el("td", { text: String(pod.restarts) }),
                    el("td", { class: "mono", text: pod.node }),
                    el("td", { class: "mono", text: pod.ip }),
                    el("td", { text: duration(pod.age_seconds) }),
                ),
            )
            : [el("tr", {}, el("td", { colspan: "7", text: "No pods match that filter." }))]),
    );
}

function renderEvents() {
    const list = $("#eventList");

    if (!data.events.length) {
        list.replaceChildren(
            el("p", { class: "empty", text: "No recent events. They appear when pods start, stop or fail." }),
        );
        return;
    }

    list.replaceChildren(
        ...data.events.map((event) =>
            el("div", { class: "event" },
                el("span", { class: `event-type ${event.type.toLowerCase()}`, text: event.type }),
                el("div", { class: "event-body" },
                    el("strong", { text: event.reason }),
                    el("p", { text: event.message }),
                    el("code", { text: event.object }),
                ),
                el("span", {
                    class: "event-age",
                    text: `${duration(event.age_seconds)} ago${event.count > 1 ? `, x${event.count}` : ""}`,
                }),
            ),
        ),
    );
}

function render() {
    renderBar();
    renderHero();
    renderGauges();
    renderBand();
    renderTopology();
    renderPodInfo();
    renderPods();
    renderEvents();
}

/* ---------- Loading data ---------- */
async function refresh() {
    const started = performance.now();
    const status = $("#updated");

    try {
        const response = await fetch("/api/dashboard", { cache: "no-store" });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        data = await response.json();
        render();

        status.className = "";
        status.textContent = `Updated ${clock()}, ${Math.round(performance.now() - started)} ms`;
    } catch (error) {
        status.className = "bad";
        status.textContent = "Connection lost, retrying";
    }
}

function schedule() {
    clearInterval(timer);
    if (live) timer = setInterval(() => !document.hidden && refresh(), 5000);
}

$("#liveToggle").addEventListener("click", (event) => {
    live = !live;
    event.currentTarget.setAttribute("aria-pressed", String(live));
    event.currentTarget.textContent = live ? "Live" : "Paused";
    schedule();
    if (live) refresh();
});

document.addEventListener("visibilitychange", () => {
    if (!document.hidden && live) refresh();
});

$("#podFilter").addEventListener("input", () => data && renderPods());

/* ---------- Ask the service again ---------- */
$("#askAgain").addEventListener("click", async () => {
    const result = $("#askResult");
    result.textContent = "Asking...";

    try {
        const response = await fetch("/api/whoami", { cache: "no-store" });
        const me = await response.json();
        const previous = data && data.me.pod;

        result.textContent =
            me.pod === previous
                ? "The same pod answered. Browsers reuse connections, so this is common."
                : "A different pod answered.";

        if (data) {
            data.me = me;
            renderHero();
            renderTopology();
        } else {
            seen.add(me.pod);
            renderSeen();
        }
    } catch (error) {
        result.textContent = "The service did not answer. Try again.";
    }
});

/* ---------- Copy buttons in the deploy guide ---------- */
$$(".copy").forEach((button) => {
    button.addEventListener("click", async () => {
        const text = $("code", button.parentElement).textContent;

        try {
            await navigator.clipboard.writeText(text);
            button.textContent = "Copied";
        } catch (error) {
            const helper = el("textarea", {});
            helper.value = text;
            document.body.append(helper);
            helper.select();
            const copied = document.execCommand("copy");
            helper.remove();
            button.textContent = copied ? "Copied" : "Press Ctrl+C";
        }

        setTimeout(() => { button.textContent = "Copy"; }, 1600);
    });
});

/* ---------- Start ---------- */
route();
refresh();
schedule();
