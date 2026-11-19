import { useCallback, useEffect, useRef, useState } from "react";
import { GITHUB_API_REPO_URL, SHIELDS_STARS_URL } from "../data/siteContent";

const STORAGE_KEY = "ubsi-skill-star-unlocked-v1";

async function fetchLiveStarCount() {
  try {
    const res = await fetch(GITHUB_API_REPO_URL, {
      cache: "no-store",
      headers: { Accept: "application/vnd.github+json" },
    });
    if (res.ok) {
      const data = await res.json();
      if (typeof data.stargazers_count === "number") {
        return { ok: true, count: data.stargazers_count, source: "github" };
      }
    }
  } catch {
    // Fall through to Shields JSON mirror if GitHub API is temporarily unreachable
  }

  try {
    const res2 = await fetch(SHIELDS_STARS_URL, { cache: "no-store" });
    if (res2.ok) {
      const data2 = await res2.json();
      const parsed = Number.parseInt(String(data2.message || "0").replace(/[^0-9]/g, ""), 10);
      if (!Number.isNaN(parsed)) {
        return { ok: true, count: parsed, source: "shields" };
      }
    }
  } catch {
    // Both endpoints unreachable
  }

  return { ok: false, count: null, source: "offline" };
}

export function useStarGate() {
  const [unlocked, setUnlocked] = useState(() => {
    try {
      return localStorage.getItem(STORAGE_KEY) === "1";
    } catch {
      return false;
    }
  });
  const [starCount, setStarCount] = useState(null);
  const [gatePhase, setGatePhase] = useState("locked"); // locked | waiting | checking | not_yet | existing_confirm | error
  const [statusMessage, setStatusMessage] = useState("");

  const baselineRef = useRef(null);
  const visitedRepoAtRef = useRef(0);
  const retryTimersRef = useRef([]);

  const clearRetryTimers = useCallback(() => {
    retryTimersRef.current.forEach((id) => window.clearTimeout(id));
    retryTimersRef.current = [];
  }, []);

  const markUnlocked = useCallback((newCount) => {
    clearRetryTimers();
    if (typeof newCount === "number") {
      setStarCount(newCount);
    }
    setUnlocked(true);
    setGatePhase("locked");
    setStatusMessage("");
    try {
      localStorage.setItem(STORAGE_KEY, "1");
    } catch {
      // Ignore storage restriction
    }
  }, [clearRetryTimers]);

  // Initial live baseline fetch & 0-star honesty guard
  useEffect(() => {
    let alive = true;
    fetchLiveStarCount().then((res) => {
      if (!alive || !res.ok || res.count === null) return;
      setStarCount(res.count);
      if (baselineRef.current === null) {
        baselineRef.current = res.count;
      }
      // Strict guard: if repository genuinely has 0 stars on GitHub, lock cannot remain open
      if (res.count === 0) {
        setUnlocked(false);
        try {
          localStorage.removeItem(STORAGE_KEY);
        } catch {
          // Ignore
        }
      }
    });
    return () => {
      alive = false;
      clearRetryTimers();
    };
  }, [clearRetryTimers]);

  const verifyStarsNow = useCallback(
    async ({ allowExistingStar = false, silentRetry = false } = {}) => {
      if (unlocked) return true;
      if (!silentRetry) {
        setGatePhase("checking");
        setStatusMessage("Memeriksa jumlah bintang langsung dari GitHub API...");
      }

      const res = await fetchLiveStarCount();
      if (!res.ok || res.count === null) {
        setGatePhase("error");
        setStatusMessage(
          "Gagal menghubungi GitHub API (batas kuota jaringan atau koneksi terputus). Pastikan Anda sudah menekan Star di GitHub lalu coba periksa kembali."
        );
        return false;
      }

      setStarCount(res.count);
      const base = baselineRef.current ?? 0;

      // 1. Strictly reject when repo still has 0 stars
      if (res.count === 0) {
        setGatePhase("not_yet");
        setStatusMessage(
          "Tercatat masih 0 bintang di Sutannn13/laporan-generator. Klik tombol Star di pojok kanan atas halaman GitHub terlebih dahulu, lalu periksa kembali."
        );
        return false;
      }

      // 2. Genuine star increment detected (count increased above baseline!)
      if (res.count > base) {
        markUnlocked(res.count);
        return true;
      }

      // 3. Repo has >= 1 stars, and user already starred previously before loading this page
      if (allowExistingStar && res.count >= 1 && visitedRepoAtRef.current > 0) {
        markUnlocked(res.count);
        return true;
      }

      setGatePhase("existing_confirm");
      setStatusMessage(
        `Saat ini repositori memiliki ${res.count} bintang (sinkronisasi API GitHub terkadang jeda beberapa detik). Jika Anda baru saja atau sudah pernah menekan Star sebelumnya, klik Konfirmasi & Buka.`
      );
      return false;
    },
    [markUnlocked, unlocked]
  );

  const registerRepoVisit = useCallback(() => {
    visitedRepoAtRef.current = Date.now();
    if (!unlocked) {
      setGatePhase("waiting");
      setStatusMessage(
        "Halaman GitHub terbuka di tab baru. Silakan tekan tombol Star di sana, lalu kembali ke halaman ini."
      );
    }
  }, [unlocked]);

  // Auto-verify when user returns from GitHub tab to this tab
  useEffect(() => {
    if (unlocked) return undefined;

    const onReturnToTab = () => {
      if (document.visibilityState === "hidden") return;
      if (visitedRepoAtRef.current <= 0) return;
      if (Date.now() - visitedRepoAtRef.current < 1200) return;

      clearRetryTimers();
      verifyStarsNow({ allowExistingStar: false, silentRetry: false }).then((passed) => {
        if (!passed) {
          // GitHub API CDN can lag 2-5s right after clicking Star; schedule two quiet re-checks
          const t1 = window.setTimeout(() => {
            verifyStarsNow({ allowExistingStar: false, silentRetry: true });
          }, 2800);
          const t2 = window.setTimeout(() => {
            verifyStarsNow({ allowExistingStar: false, silentRetry: true });
          }, 6200);
          retryTimersRef.current.push(t1, t2);
        }
      });
    };

    window.addEventListener("focus", onReturnToTab);
    document.addEventListener("visibilitychange", onReturnToTab);
    return () => {
      window.removeEventListener("focus", onReturnToTab);
      document.removeEventListener("visibilitychange", onReturnToTab);
    };
  }, [clearRetryTimers, unlocked, verifyStarsNow]);

  return {
    unlocked,
    starCount,
    gatePhase,
    statusMessage,
    hasVisitedRepo: visitedRepoAtRef.current > 0,
    registerRepoVisit,
    verifyStarsNow,
  };
}
