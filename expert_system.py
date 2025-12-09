"""CLI expert system untuk rekomendasi jurusan kuliah berbasis forward chaining.
"""
from dataclasses import dataclass
from typing import Callable, Dict, List, Set, Tuple
import sys
import unittest


@dataclass
class Rule:
    name: str
    major: str
    weight: float
    condition: Callable[[Dict[str, object]], Tuple[bool, str]]


class KnowledgeBase:
    def __init__(self) -> None:
        self.rules: List[Rule] = self._build_rules()
        self.total_weight_per_major: Dict[str, float] = self._compute_total_weights()

    def _build_rules(self) -> List[Rule]:
        return [
            Rule(
                name="TI-Interes-Investigative",
                major="Teknik Informatika",
                weight=0.25,
                condition=lambda f: (
                    "Investigative" in f["interests"] and f["math"] >= 85,
                    "Minat Investigative dan nilai Matematika tinggi mendukung logika pemrograman.",
                ),
            ),
            Rule(
                name="TI-Environment-Industry",
                major="Teknik Informatika",
                weight=0.2,
                condition=lambda f: (
                    f["environment"] in {"industri", "riset"},
                    "Preferensi lingkungan industri/riset cocok dengan proyek pengembangan perangkat lunak.",
                ),
            ),
            Rule(
                name="TI-Career-Tech",
                major="Teknik Informatika",
                weight=0.15,
                condition=lambda f: (
                    any(k in f["career_goal"] for k in ["developer", "software", "data", "AI", "robot"]),
                    "Tujuan karier di bidang teknologi sesuai dengan proyeksi TI.",
                ),
            ),
            Rule(
                name="TI-Creative-Blend",
                major="Teknik Informatika",
                weight=0.15,
                condition=lambda f: (
                    f["environment"] == "kreatif" and "Artistic" in f["interests"],
                    "Kombinasi lingkungan kreatif dan minat Artistic membuka jalur UI/UX dan front-end.",
                ),
            ),
            Rule(
                name="SI-Structured",
                major="Sistem Informasi",
                weight=0.25,
                condition=lambda f: (
                    "Conventional" in f["interests"] and f["math"] >= 75,
                    "Minat Conventional dan dasar Matematika memadai untuk analisis sistem.",
                ),
            ),
            Rule(
                name="SI-Industry",
                major="Sistem Informasi",
                weight=0.2,
                condition=lambda f: (
                    f["environment"] == "industri",
                    "Preferensi industri cocok dengan penerapan SI di organisasi.",
                ),
            ),
            Rule(
                name="SI-Career-BusinessIT",
                major="Sistem Informasi",
                weight=0.15,
                condition=lambda f: (
                    any(k in f["career_goal"] for k in ["analyst", "bisnis", "system"]),
                    "Tujuan karier analisis sistem/teknologi bisnis mendukung SI.",
                ),
            ),
            Rule(
                name="Elektro-STEM",
                major="Teknik Elektro",
                weight=0.3,
                condition=lambda f: (
                    "Realistic" in f["interests"] and f["math"] >= 80 and f["physics"] >= 80,
                    "Minat Realistic dan nilai Matematika/Fisika tinggi penting untuk rekayasa listrik.",
                ),
            ),
            Rule(
                name="Elektro-Riset",
                major="Teknik Elektro",
                weight=0.2,
                condition=lambda f: (
                    f["environment"] in {"industri", "riset"},
                    "Preferensi riset/industri sejalan dengan eksperimen elektronika.",
                ),
            ),
            Rule(
                name="Mesin-STEM",
                major="Teknik Mesin",
                weight=0.3,
                condition=lambda f: (
                    "Realistic" in f["interests"] and f["math"] >= 75 and f["physics"] >= 75,
                    "Minat Realistic dan dasar Matematika/Fisika baik untuk mekanika.",
                ),
            ),
            Rule(
                name="Mesin-Industry",
                major="Teknik Mesin",
                weight=0.2,
                condition=lambda f: (
                    f["environment"] == "industri",
                    "Preferensi industri cocok dengan manufaktur dan produksi.",
                ),
            ),
            Rule(
                name="Kedokteran-Bio",
                major="Kedokteran",
                weight=0.35,
                condition=lambda f: (
                    "Social" in f["interests"] and f["biology"] >= 85 and f["chemistry"] >= 80,
                    "Minat Social serta nilai Biologi/Kimia tinggi diperlukan untuk profesi dokter.",
                ),
            ),
            Rule(
                name="Kedokteran-Career",
                major="Kedokteran",
                weight=0.2,
                condition=lambda f: (
                    any(k in f["career_goal"] for k in ["dokter", "medis", "kesehatan"]),
                    "Tujuan karier medis menguatkan pilihan Kedokteran.",
                ),
            ),
            Rule(
                name="Farmasi-Science",
                major="Farmasi",
                weight=0.3,
                condition=lambda f: (
                    "Investigative" in f["interests"] and f["chemistry"] >= 85,
                    "Minat Investigative dan nilai Kimia tinggi sesuai eksperimen obat.",
                ),
            ),
            Rule(
                name="Farmasi-Bio",
                major="Farmasi",
                weight=0.2,
                condition=lambda f: (
                    f["biology"] >= 80,
                    "Penguasaan Biologi mendukung pemahaman farmakologi.",
                ),
            ),
            Rule(
                name="Farmasi-Career",
                major="Farmasi",
                weight=0.15,
                condition=lambda f: (
                    any(k in f["career_goal"] for k in ["farmasi", "apotek", "apoteker", "obat"]),
                    "Tujuan karier di bidang farmasi memperkuat kecocokan.",
                ),
            ),
            Rule(
                name="Keperawatan-Social",
                major="Keperawatan",
                weight=0.3,
                condition=lambda f: (
                    "Social" in f["interests"] and f["biology"] >= 80,
                    "Minat Social dan Biologi tinggi mendukung perawatan pasien.",
                ),
            ),
            Rule(
                name="Keperawatan-Career",
                major="Keperawatan",
                weight=0.2,
                condition=lambda f: (
                    any(k in f["career_goal"] for k in ["perawat", "care", "nurse"]),
                    "Tujuan karier keperawatan memperkuat pilihan.",
                ),
            ),
            Rule(
                name="Biologi-Riset",
                major="Biologi",
                weight=0.3,
                condition=lambda f: (
                    "Investigative" in f["interests"] and f["biology"] >= 85,
                    "Minat Investigative dan nilai Biologi tinggi cocok untuk riset hayati.",
                ),
            ),
            Rule(
                name="Biologi-Environment",
                major="Biologi",
                weight=0.2,
                condition=lambda f: (
                    f["environment"] == "riset",
                    "Preferensi riset mendukung kegiatan laboratorium Biologi.",
                ),
            ),
            Rule(
                name="Kimia-Riset",
                major="Kimia",
                weight=0.3,
                condition=lambda f: (
                    "Investigative" in f["interests"] and f["chemistry"] >= 85,
                    "Minat Investigative dan Kimia tinggi diperlukan untuk riset kimia.",
                ),
            ),
            Rule(
                name="Kimia-Environment",
                major="Kimia",
                weight=0.2,
                condition=lambda f: (
                    f["environment"] == "riset",
                    "Preferensi riset sesuai eksperimen laboratorium Kimia.",
                ),
            ),
            Rule(
                name="Kimia-Career",
                major="Kimia",
                weight=0.15,
                condition=lambda f: (
                    any(k in f["career_goal"] for k in ["kimia", "chemist", "laboratorium"]),
                    "Tujuan karier kimia memperkuat fokus eksperimen dan sintesis.",
                ),
            ),
            Rule(
                name="Hukum-Social",
                major="Hukum",
                weight=0.3,
                condition=lambda f: (
                    ("Enterprising" in f["interests"] or "Social" in f["interests"]) and f["language"] >= 80,
                    "Minat Enterprising/Social serta Bahasa tinggi penting untuk advokasi hukum.",
                ),
            ),
            Rule(
                name="Hukum-Career",
                major="Hukum",
                weight=0.2,
                condition=lambda f: (
                    any(k in f["career_goal"] for k in ["hukum", "law", "advokat", "jaksa"]),
                    "Tujuan karier hukum memperkuat pilihan.",
                ),
            ),
            Rule(
                name="Psikologi-Social",
                major="Psikologi",
                weight=0.3,
                condition=lambda f: (
                    ("Social" in f["interests"] or "Artistic" in f["interests"]) and f["language"] >= 78,
                    "Minat Social/Artistic dan Bahasa memadai untuk komunikasi psikologi.",
                ),
            ),
            Rule(
                name="Psikologi-Career",
                major="Psikologi",
                weight=0.2,
                condition=lambda f: (
                    any(k in f["career_goal"] for k in ["psiko", "konselor", "terapis"]),
                    "Tujuan karier konseling/terapi sesuai Psikologi.",
                ),
            ),
            Rule(
                name="Akuntansi-Conventional",
                major="Akuntansi",
                weight=0.3,
                condition=lambda f: (
                    "Conventional" in f["interests"] and f["math"] >= 78,
                    "Minat Conventional dan Matematika tinggi mendukung pencatatan keuangan.",
                ),
            ),
            Rule(
                name="Akuntansi-Career",
                major="Akuntansi",
                weight=0.2,
                condition=lambda f: (
                    "akuntan" in f["career_goal"],
                    "Tujuan karier akuntan memperkuat jurusan.",
                ),
            ),
            Rule(
                name="Manajemen-Enterprising",
                major="Manajemen",
                weight=0.25,
                condition=lambda f: (
                    "Enterprising" in f["interests"] and f["math"] >= 75,
                    "Minat Enterprising dan dasar numerik baik untuk pengambilan keputusan bisnis.",
                ),
            ),
            Rule(
                name="Manajemen-Industry",
                major="Manajemen",
                weight=0.15,
                condition=lambda f: (
                    f["environment"] == "industri",
                    "Preferensi industri sesuai praktik manajerial perusahaan.",
                ),
            ),
            Rule(
                name="Manajemen-Career",
                major="Manajemen",
                weight=0.15,
                condition=lambda f: (
                    any(k in f["career_goal"] for k in ["manager", "bisnis", "entrepreneur"]),
                    "Tujuan karier manajerial/bisnis mendukung jurusan.",
                ),
            ),
            Rule(
                name="Ekonomi-Analyst",
                major="Ekonomi",
                weight=0.25,
                condition=lambda f: (
                    ("Investigative" in f["interests"] or "Enterprising" in f["interests"]) and f["math"] >= 75,
                    "Minat Investigative/Enterprising serta Matematika cukup untuk analisis ekonomi.",
                ),
            ),
            Rule(
                name="Ekonomi-Career",
                major="Ekonomi",
                weight=0.15,
                condition=lambda f: (
                    any(k in f["career_goal"] for k in ["ekonomi", "analis", "riset pasar"]),
                    "Tujuan karier analis ekonomi memperkuat jurusan.",
                ),
            ),
            Rule(
                name="Statistika-StrongMath",
                major="Statistika",
                weight=0.35,
                condition=lambda f: (
                    "Investigative" in f["interests"] and f["math"] >= 88,
                    "Minat Investigative dan Matematika sangat tinggi kunci Statistika.",
                ),
            ),
            Rule(
                name="Statistika-Riset",
                major="Statistika",
                weight=0.2,
                condition=lambda f: (
                    f["environment"] == "riset",
                    "Preferensi riset sesuai pengembangan model statistik.",
                ),
            ),
            Rule(
                name="Statistika-Career",
                major="Statistika",
                weight=0.15,
                condition=lambda f: (
                    any(k in f["career_goal"] for k in ["statistik", "data", "analitik"]),
                    "Tujuan karier analitik/data science mendukung Statistika.",
                ),
            ),
            Rule(
                name="DKV-Art",
                major="Desain Komunikasi Visual",
                weight=0.35,
                condition=lambda f: (
                    "Artistic" in f["interests"] and f["environment"] == "kreatif",
                    "Minat Artistic dan lingkungan kreatif identik dengan DKV.",
                ),
            ),
            Rule(
                name="DKV-Career",
                major="Desain Komunikasi Visual",
                weight=0.2,
                condition=lambda f: (
                    any(k in f["career_goal"] for k in ["desain", "designer", "grafis"]),
                    "Tujuan karier desain memperkuat jurusan DKV.",
                ),
            ),
        ]

    def _compute_total_weights(self) -> Dict[str, float]:
        totals: Dict[str, float] = {}
        for rule in self.rules:
            totals[rule.major] = totals.get(rule.major, 0.0) + rule.weight
        return totals


@dataclass
class FiredRule:
    rule: Rule
    explanation: str


class InferenceEngine:
    def __init__(self, kb: KnowledgeBase) -> None:
        self.kb = kb

    def infer(self, facts: Dict[str, object]) -> List[FiredRule]:
        fired: List[FiredRule] = []
        for rule in self.kb.rules:
            result, explanation = rule.condition(facts)
            if result:
                fired.append(FiredRule(rule=rule, explanation=explanation))
        return fired


class Recommender:
    def __init__(self, kb: KnowledgeBase, engine: InferenceEngine) -> None:
        self.kb = kb
        self.engine = engine

    def recommend(self, facts: Dict[str, object], top_n: int = 3) -> List[Dict[str, object]]:
        fired_rules = self.engine.infer(facts)
        matched_weight: Dict[str, float] = {major: 0.0 for major in self.kb.total_weight_per_major}
        contributing_rules: Dict[str, List[FiredRule]] = {major: [] for major in self.kb.total_weight_per_major}

        for fired in fired_rules:
            matched_weight[fired.rule.major] += fired.rule.weight
            contributing_rules[fired.rule.major].append(fired)

        recommendations: List[Dict[str, object]] = []
        for major, total_weight in self.kb.total_weight_per_major.items():
            if total_weight == 0:
                continue
            score = matched_weight[major] / total_weight
            if matched_weight[major] == 0:
                continue
            recommendations.append(
                {
                    "major": major,
                    "score": round(score, 3),
                    "details": contributing_rules[major],
                    "matched_weight": matched_weight[major],
                    "total_weight": total_weight,
                }
            )

        recommendations.sort(
            key=lambda r: (r["score"], r["matched_weight"]),
            reverse=True,
        )
        return recommendations[:top_n]


class CLI:
    VALID_INTERESTS = {"Realistic", "Investigative", "Artistic", "Social", "Enterprising", "Conventional"}
    VALID_STYLES = {"visual", "auditori", "kinestetik"}
    VALID_ENVIRONMENTS = {"riset", "industri", "kreatif"}

    def __init__(self) -> None:
        self.kb = KnowledgeBase()
        self.engine = InferenceEngine(self.kb)
        self.recommender = Recommender(self.kb, self.engine)

    def run(self) -> None:
        print("=== Rekomendasi Jurusan Kuliah (Expert System) ===")
        interests = self._ask_interests()
        grades = self._ask_grades()
        learning_style = self._ask_option("Gaya belajar (visual/auditori/kinestetik)", self.VALID_STYLES)
        environment = self._ask_option("Preferensi lingkungan (riset/industri/kreatif)", self.VALID_ENVIRONMENTS)
        career_goal = input("Tujuan karier (contoh: dokter, developer, analis data): ").strip().lower()

        facts = {
            "interests": interests,
            "math": grades["math"],
            "physics": grades["physics"],
            "biology": grades["biology"],
            "chemistry": grades["chemistry"],
            "language": grades["language"],
            "learning_style": learning_style,
            "environment": environment,
            "career_goal": career_goal,
        }

        recommendations = self.recommender.recommend(facts)
        self._display_results(recommendations)

    def _ask_interests(self) -> Set[str]:
        while True:
            raw = input(
                "Minat RIASEC (pisahkan dengan koma, contoh: Investigative,Realistic): "
            ).strip()
            interests = {part.strip().capitalize() for part in raw.split(",") if part.strip()}
            if interests and interests.issubset(self.VALID_INTERESTS):
                return interests
            print(f"Input tidak valid. Pilihan: {', '.join(sorted(self.VALID_INTERESTS))}.")

    def _ask_grades(self) -> Dict[str, float]:
        return {
            "math": self._ask_grade("Nilai Matematika"),
            "physics": self._ask_grade("Nilai Fisika"),
            "biology": self._ask_grade("Nilai Biologi"),
            "chemistry": self._ask_grade("Nilai Kimia"),
            "language": self._ask_grade("Nilai Bahasa"),
        }

    def _ask_grade(self, prompt: str) -> float:
        while True:
            raw = input(f"{prompt} (0-100): ").strip()
            if raw.isdigit():
                value = int(raw)
                if 0 <= value <= 100:
                    return float(value)
            print("Nilai harus berupa angka 0-100.")

    def _ask_option(self, prompt: str, valid_options: Set[str]) -> str:
        while True:
            value = input(f"{prompt}: ").strip().lower()
            if value in valid_options:
                return value
            print(f"Pilihan tidak valid. Gunakan salah satu: {', '.join(sorted(valid_options))}.")

    def _display_results(self, recommendations: List[Dict[str, object]]) -> None:
        if not recommendations:
            print("Maaf, belum ada rekomendasi berdasarkan data yang diberikan.")
            return

        print("\nRekomendasi teratas:")
        for idx, rec in enumerate(recommendations, start=1):
            print(f"{idx}. {rec['major']} (skor: {rec['score']})")
            print("   Alasan:")
            for fired in rec["details"]:
                print(f"   - Rule {fired.rule.name} (CF {fired.rule.weight}): {fired.explanation}")
            print()


def build_recommender() -> Recommender:
    kb = KnowledgeBase()
    engine = InferenceEngine(kb)
    return Recommender(kb, engine)


class RecommendationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.recommender = build_recommender()

    def test_stem_strength(self) -> None:
        facts = {
            "interests": {"Investigative", "Realistic"},
            "math": 95,
            "physics": 92,
            "biology": 80,
            "chemistry": 90,
            "language": 78,
            "learning_style": "visual",
            "environment": "riset",
            "career_goal": "insinyur robotik",
        }
        recs = self.recommender.recommend(facts)
        majors = [r["major"] for r in recs]
        self.assertIn("Teknik Elektro", majors)
        self.assertIn("Teknik Informatika", majors)
        self.assertIn("Statistika", majors)
        self.assertEqual(recs[0]["major"], "Teknik Elektro")

    def test_medical_strength(self) -> None:
        facts = {
            "interests": {"Social", "Investigative"},
            "math": 75,
            "physics": 70,
            "biology": 95,
            "chemistry": 92,
            "language": 80,
            "learning_style": "auditori",
            "environment": "riset",
            "career_goal": "dokter spesialis",
        }
        recs = self.recommender.recommend(facts)
        self.assertGreater(len(recs), 0)
        self.assertEqual(recs[0]["major"], "Kedokteran")

    def test_art_design_strength(self) -> None:
        facts = {
            "interests": {"Artistic", "Enterprising"},
            "math": 70,
            "physics": 60,
            "biology": 65,
            "chemistry": 60,
            "language": 85,
            "learning_style": "visual",
            "environment": "kreatif",
            "career_goal": "desainer grafis",
        }
        recs = self.recommender.recommend(facts)
        self.assertGreater(len(recs), 0)
        self.assertEqual(recs[0]["major"], "Desain Komunikasi Visual")


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(RecommendationTests)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        sys.exit(not result.wasSuccessful())
    CLI().run()


if __name__ == "__main__":
    main()
