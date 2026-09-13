import json
import os

advisory = {
    "Apple___Apple_scab": {
        "crop": "Apple",
        "condition": "Apple Scab",
        "pathogen": "Venturia inaequalis (Fungus)",
        "type": "Fungal",
        "severity": "Moderate to High",
        "symptoms": [
            "Olive-green to velvety brown circular spots on upper leaf surfaces.",
            "Leaf distortion, puckering, and premature leaf drop.",
            "Corky, scab-like lesions on maturing fruit."
        ],
        "organic_solutions": [
            "Spray liquid copper soap or sulfur early in the season before bud break.",
            "Apply Bacillus subtilis or neem oil as preventative foliar bio-fungicides.",
            "Rake and shred or compost fallen autumn leaves to eliminate overwintering spores."
        ],
        "chemical_solutions": [
            "Apply systemic fungicides such as Difenoconazole or Myclobutanil at green tip stage.",
            "Use protective fungicides like Captan or Mancozeb before anticipated rain periods."
        ],
        "fertilizer_advice": [
            "Avoid excessive spring nitrogen application, which causes rapid tender shoot growth prone to infection.",
            "Ensure adequate soil potassium and zinc levels to boost foliar cuticle resistance."
        ],
        "prevention": [
            "Prune dense canopy branches annually to improve internal airflow and sunlight penetration.",
            "Plant scab-resistant apple cultivars such as Liberty, Enterprise, or Freedom."
        ]
    },
    "Apple___Black_rot": {
        "crop": "Apple",
        "condition": "Black Rot (Frogeye Leaf Spot)",
        "pathogen": "Botryosphaeria obtusa (Fungus)",
        "type": "Fungal",
        "severity": "High",
        "symptoms": [
            "Small purple specks on leaves expanding into circular spots with light tan centers and dark margins (frogeye spot).",
            "Severe leaf yellowing and defoliation in midsummer.",
            "Firm black rot on fruit and cankers on branches."
        ],
        "organic_solutions": [
            "Prune out dead wood, fire blight strikes, and mummified fruit where the fungus overwinters.",
            "Spray copper hydroxide or lime-sulfur during dormant or silver tip bud stages."
        ],
        "chemical_solutions": [
            "Apply Captan or Thiophanate-methyl from tight cluster through cover sprays.",
            "Rotate FRAC group 3 and 11 fungicides to prevent fungal resistance."
        ],
        "fertilizer_advice": [
            "Provide balanced N-P-K (10-10-10) fertilizer based on soil tests; avoid excess nitrogen.",
            "Apply foliar boron and calcium during fruit development to maintain tissue vigor."
        ],
        "prevention": [
            "Remove all mummified apples remaining in the tree or on the ground after harvest.",
            "Sterilize pruning shears with 70% isopropyl alcohol between trees."
        ]
    },
    "Apple___Cedar_apple_rust": {
        "crop": "Apple",
        "condition": "Cedar Apple Rust",
        "pathogen": "Gymnosporangium juniperi-virginianae (Fungus)",
        "type": "Fungal",
        "severity": "Moderate",
        "symptoms": [
            "Bright yellow-orange or reddish spots on upper leaf surfaces.",
            "Minute black fungal bodies inside orange spots, with tube-like aecia forming on leaf undersides.",
            "Premature leaf fall in susceptible varieties during warm, rainy spring weather."
        ],
        "organic_solutions": [
            "Apply sulfur or copper fungicides starting at pink bud stage until petal fall.",
            "Physically prune out eastern red cedar galls within several hundred yards of orchard if possible."
        ],
        "chemical_solutions": [
            "Spray Myclobutanil (Immunox) or Propiconazole at 7-10 day intervals from pink bud stage.",
            "Mancozeb can be applied as a protectant early in the season."
        ],
        "fertilizer_advice": [
            "Ensure adequate potassium to strengthen leaf epidermis against fungal tube penetration.",
            "Maintain steady micronutrient balance (magnesium and zinc) to reduce foliar stress."
        ],
        "prevention": [
            "Plant rust-resistant apple varieties such as Redfree, William's Pride, or Pristine.",
            "Eliminate or isolate nearby juniper / red cedar trees which act as alternate hosts."
        ]
    },
    "Apple___healthy": {
        "crop": "Apple",
        "condition": "Healthy Apple Foliage",
        "pathogen": "None (Healthy Plant)",
        "type": "Healthy",
        "severity": "None",
        "symptoms": [
            "Vibrant, deep-green leaves with crisp margins and unblemished surface.",
            "Uniform leaf growth without spots, curling, wilting, or powdery mildew."
        ],
        "organic_solutions": [
            "Maintain regular preventive sprays of compost tea or dilute seaweed extract to stimulate beneficial phyllosphere microbes."
        ],
        "chemical_solutions": [
            "No chemical fungicides or bactericides required."
        ],
        "fertilizer_advice": [
            "Apply organic compost or balanced slow-release fertilizer in early spring.",
            "Monitor soil pH between 6.0 and 7.0 for optimal micronutrient uptake."
        ],
        "prevention": [
            "Continue regular dormant pruning and monitor weekly for early insect or fungal signs.",
            "Maintain a 3-4 inch layer of organic mulch around tree drip line to preserve moisture."
        ]
    },
    "Pepper,_bell___Bacterial_spot": {
        "crop": "Bell Pepper",
        "condition": "Bacterial Spot",
        "pathogen": "Xanthomonas campestris pv. vesicatoria (Bacteria)",
        "type": "Bacterial",
        "severity": "High",
        "symptoms": [
            "Small, water-soaked, yellowish-green spots on leaves turning dark brown with greasy margins.",
            "Corky raised spots on fruit that can lead to secondary rot.",
            "Extensive leaf drop leaving fruit exposed to sunscald."
        ],
        "organic_solutions": [
            "Apply fixed copper bactericides combined with bio-fungicide (Bacillus amyloliquefaciens).",
            "Hot water treat seeds (50°C for 25 minutes) prior to sowing to eradicate seed-borne bacteria."
        ],
        "chemical_solutions": [
            "Spray copper hydroxide tank-mixed with Mancozeb to combat copper-resistant bacterial strains.",
            "Apply Actigard (acibenzolar-S-methyl) as a plant defense activator before disease onset."
        ],
        "fertilizer_advice": [
            "Avoid heavy nitrogen sidedressing which promotes soft, succulent leaf tissue vulnerable to bacteria.",
            "Ensure adequate calcium and phosphorus for strong cell wall development."
        ],
        "prevention": [
            "Avoid overhead sprinkler irrigation; use drip lines to keep foliage completely dry.",
            "Enforce a strict 3-year crop rotation avoiding all solanaceous plants (tomatoes, eggplants)."
        ]
    },
    "Pepper,_bell___healthy": {
        "crop": "Bell Pepper",
        "condition": "Healthy Bell Pepper Foliage",
        "pathogen": "None (Healthy Plant)",
        "type": "Healthy",
        "severity": "None",
        "symptoms": [
            "Glossy, uniformly green leaves with clean veins and strong erect stem growth.",
            "No chlorosis, curling, necrosis, or bacterial spotting."
        ],
        "organic_solutions": [
            "Foliar spray with diluted kelp meal extract to support stress tolerance and vigor."
        ],
        "chemical_solutions": [
            "No chemical intervention required."
        ],
        "fertilizer_advice": [
            "Side-dress with balanced organic N-P-K (5-10-10) at flowering to encourage robust fruit set.",
            "Apply magnesium sulfate (Epsom salt: 1 tbsp/gallon) if lower leaves show minor magnesium deficiency."
        ],
        "prevention": [
            "Mulch garden beds with clean straw to prevent soil splashing onto lower foliage.",
            "Maintain consistent soil moisture to prevent blossom end rot."
        ]
    },
    "Cherry_(including_sour)___Powdery_mildew": {
        "crop": "Cherry",
        "condition": "Powdery Mildew",
        "pathogen": "Podosphaera clandestina (Fungus)",
        "type": "Fungal",
        "severity": "Moderate",
        "symptoms": [
            "White, talcum-powder-like patches on leaves and green fruit stems.",
            "Young leaves become curled, twisted, and stunted.",
            "Dull, leathery patches on cherries with potential fruit cracking."
        ],
        "organic_solutions": [
            "Spray wettable sulfur or potassium bicarbonate (Kaligreen) at 7-10 day intervals.",
            "Apply horticultural mineral oils or neem oil to smother fungal hyphae and spores."
        ],
        "chemical_solutions": [
            "Apply Quinoxyfen (Quintec) or Triflumizole (Procure) from petal fall through shuck fall.",
            "Rotate with Boscalid/Pyraclostrobin (Pristine) to prevent chemical tolerance."
        ],
        "fertilizer_advice": [
            "Limit high-nitrogen fertilizers that generate late flushes of tender susceptible foliage.",
            "Ensure adequate potassium and silica to strengthen epidermal cell structure."
        ],
        "prevention": [
            "Prune tree interiors to increase light penetration and air movement.",
            "Apply treatments promptly during warm, dry days with high relative humidity."
        ]
    },
    "Cherry_(including_sour)___healthy": {
        "crop": "Cherry",
        "condition": "Healthy Cherry Foliage",
        "pathogen": "None (Healthy Plant)",
        "type": "Healthy",
        "severity": "None",
        "symptoms": [
            "Bright green, firm leaves with sharp serrated edges and clean glossy surfaces.",
            "Vigorous terminal shoot growth without leaf curling or white fungal mycelium."
        ],
        "organic_solutions": [
            "Spray compost tea or fish hydrolysate foliar feeds during early vegetative phase."
        ],
        "chemical_solutions": [
            "No chemical fungicides or insecticides required."
        ],
        "fertilizer_advice": [
            "Apply balanced fruit tree fertilizer in early spring before bud break.",
            "Maintain soil pH between 6.2 and 6.8 with good organic matter."
        ],
        "prevention": [
            "Perform annual winter dormant pruning to eliminate crossing branches.",
            "Inspect canopy weekly for aphid activity or early mildew signs."
        ]
    },
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "crop": "Corn",
        "condition": "Cercospora Leaf Spot (Gray Leaf Spot)",
        "pathogen": "Cercospora zeae-maydis (Fungus)",
        "type": "Fungal",
        "severity": "High",
        "symptoms": [
            "Small, tan, rectangular lesions with sharp, parallel edges constrained by leaf veins.",
            "Lesions turn grayish-brown with fungal sporulation in humid weather.",
            "Extensive blight coalescence causing premature leaf death and stalk lodging."
        ],
        "organic_solutions": [
            "Spray bio-fungicides containing Bacillus amyloliquefaciens or Trichoderma viride.",
            "Thoroughly incorporate crop residue into soil post-harvest to accelerate fungal decay."
        ],
        "chemical_solutions": [
            "Apply strobilurin-triazole pre-mix fungicides (e.g. Azoxystrobin + Difenoconazole) at VT/R1 stage.",
            "Time spray when lesions appear on the third leaf below ear leaf or higher."
        ],
        "fertilizer_advice": [
            "Ensure adequate potassium (K) nutrition; potassium deficiency significantly aggravates gray leaf spot severity.",
            "Avoid over-applying nitrogen in single doses; use split applications."
        ],
        "prevention": [
            "Plant corn hybrids possessing high genetic resistance ratings to gray leaf spot.",
            "Implement 1-2 year crop rotation out of corn to soybeans or small grains."
        ]
    },
    "Corn_(maize)___Common_rust_": {
        "crop": "Corn",
        "condition": "Common Rust",
        "pathogen": "Puccinia sorghi (Fungus)",
        "type": "Fungal",
        "severity": "Moderate",
        "symptoms": [
            "Oval to elongate cinnamon-brown pustules scattered across both upper and lower leaf surfaces.",
            "Pustules rupture the epidermis releasing powdery reddish-brown urediniospores.",
            "Pustules turn brownish-black late in the season as teliospores develop."
        ],
        "organic_solutions": [
            "Apply sulfur or neem-based foliar sprays at earliest sign of rust pustules.",
            "Promote early canopy vigor with humic acid and seaweed soil conditioners."
        ],
        "chemical_solutions": [
            "Apply fungicides such as Azoxystrobin, Pyraclostrobin, or Propiconazole if rust appears prior to tasseling.",
            "Treat when rust pustules cover more than 5% of the upper canopy leaves."
        ],
        "fertilizer_advice": [
            "Maintain balanced N-P-K fertility; excessive nitrogen combined with low potassium increases rust susceptibility.",
            "Foliar zinc and boron boost plant disease defense enzyme pathways."
        ],
        "prevention": [
            "Plant rust-resistant hybrids carrying Rp gene resistance.",
            "Plant early in the season to complete grain fill before airborne rust spores migrate in."
        ]
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "crop": "Corn",
        "condition": "Northern Leaf Blight",
        "pathogen": "Exserohilum turcicum (Fungus)",
        "type": "Fungal",
        "severity": "High",
        "symptoms": [
            "Long, elliptical, cigar-shaped, grayish-green or tan lesions (1-6 inches long).",
            "Lesions not restricted by leaf veins, spreading freely across leaves.",
            "Dark dirty olive-colored fungal spores appearing on lesions in wet conditions."
        ],
        "organic_solutions": [
            "Foliar spray with copper fungicides or bio-fungicide formulations (Streptomyces lydicus).",
            "Till crop debris deeply into soil post-harvest to speed up saprophytic decomposition."
        ],
        "chemical_solutions": [
            "Spray fungicides containing Prothioconazole, Azoxystrobin, or Picoxystrobin between V14 and R2 growth stages.",
            "Treat if lesions are present on ear leaves or 1-2 leaves below before silking."
        ],
        "fertilizer_advice": [
            "Apply balanced fertilization based on soil analysis; avoid high nitrates.",
            "Potassium and sulfur fertilization improve natural lignin production in leaf sheaths."
        ],
        "prevention": [
            "Select hybrids containing single-gene Ht resistance or strong polygenic resistance.",
            "Rotate fields with non-host crops such as alfalfa, clover, or soybeans."
        ]
    },
    "Corn_(maize)___healthy": {
        "crop": "Corn",
        "condition": "Healthy Corn Foliage",
        "pathogen": "None (Healthy Plant)",
        "type": "Healthy",
        "severity": "None",
        "symptoms": [
            "Broad, dark green leaves with strong central midribs and clean leaf collars.",
            "Uniform vegetative canopy with no lesions, rust pustules, or chlorotic streaking."
        ],
        "organic_solutions": [
            "Apply mycorrhizal inoculants at planting to enhance root phosphorus uptake."
        ],
        "chemical_solutions": [
            "No chemical fungicides or treatments needed."
        ],
        "fertilizer_advice": [
            "Provide side-dressed nitrogen during V4-V6 active growth phase based on yield goals.",
            "Ensure adequate zinc and magnesium availability in the root zone."
        ],
        "prevention": [
            "Scout fields bi-weekly through silking stage for early detection of insect or fungal presence.",
            "Maintain optimal plant population to balance canopy ventilation and yield."
        ]
    },
    "Grape___Black_rot": {
        "crop": "Grape",
        "condition": "Black Rot",
        "pathogen": "Guignardia bidwellii (Fungus)",
        "type": "Fungal",
        "severity": "High",
        "symptoms": [
            "Small, reddish-brown circular spots on leaves with distinct dark brown borders.",
            "Tiny black pycnidia (pimples) arranged in rings inside leaf lesions.",
            "Grapes shrivel into hard, black, wrinkled mummies that remain attached to the cluster."
        ],
        "organic_solutions": [
            "Spray liquid copper or sulfur starting from early bud break until veraison.",
            "Thoroughly remove and burn or bury all overwintered mummified grapes and infected canes."
        ],
        "chemical_solutions": [
            "Apply Myclobutanil (Rally), Tebuconazole, or Mancozeb from 1-inch shoot growth through 4 weeks post-bloom.",
            "Rotate chemical classes (FRAC 3, 11, and M3) to prevent resistance development."
        ],
        "fertilizer_advice": [
            "Avoid excessive spring nitrogen which causes overcrowded foliage and high micro-humidity.",
            "Ensure adequate magnesium and potassium to support vine immunity."
        ],
        "prevention": [
            "Train vines on trellises and shoot-thin to keep canopy open to breeze and sunlight.",
            "Keep vine rows mowed and weed-free to lower morning dew retention."
        ]
    },
    "Grape___Esca_(Black_Measles)": {
        "crop": "Grape",
        "condition": "Esca (Black Measles)",
        "pathogen": "Phaeomoniella chlamydospora & Fomitiporia mediterranea (Fungal Complex)",
        "type": "Fungal",
        "severity": "High / Chronic",
        "symptoms": [
            "Tiger-stripe leaf pattern: interveinal chlorosis and yellow/red necrosis with green margins along veins.",
            "Small, dark purple or black spots (measles) on berry skins.",
            "Severe apoplexy: sudden total collapse and wilting of the vine during midsummer heat."
        ],
        "organic_solutions": [
            "Apply Trichoderma-based bio-protectants directly onto fresh pruning wounds within 24 hours.",
            "Remedial vine surgery: cut trunk below visible wood necrosis and retrain a new healthy sucker."
        ],
        "chemical_solutions": [
            "Paint or spray pruning wounds with wound sealants containing Thiophanate-methyl or Boron.",
            "No cure exists once internal trunk heartwood is colonized; prevention during pruning is vital."
        ],
        "fertilizer_advice": [
            "Avoid water stress and nutrient imbalances that accelerate fungal trunk colonization.",
            "Apply moderate potassium to maintain vascular hydration and transport."
        ],
        "prevention": [
            "Delay pruning until late winter when bleeding sap cleanses wounds and wound healing is faster.",
            "Disinfect pruning loppers and saws between individual vines."
        ]
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "crop": "Grape",
        "condition": "Leaf Blight (Isariopsis Leaf Spot)",
        "pathogen": "Pseudocercospora cladosporioides / Phaeoisariopsis vitis (Fungus)",
        "type": "Fungal",
        "severity": "Moderate",
        "symptoms": [
            "Irregular, dark brown or black angular spots on leaves, often surrounded by chlorotic halos.",
            "Foliage turns yellow, dries up, and falls prematurely in late summer.",
            "Weakened vines with reduced sugar accumulation in grapes."
        ],
        "organic_solutions": [
            "Apply Bordeaux mixture (copper sulfate + slaked lime) post-bloom.",
            "Spray neem oil or bio-fungicides to suppress late-season foliar sporulation."
        ],
        "chemical_solutions": [
            "Spray Mancozeb, Captan, or Chlorothalonil when spots first appear on lower canopy.",
            "Use Strobilurin fungicides (Kresoxim-methyl or Pyraclostrobin) during humid periods."
        ],
        "fertilizer_advice": [
            "Ensure adequate zinc, iron, and potassium to prevent premature senescence.",
            "Do not over-fertilize with nitrogen late in the growing season."
        ],
        "prevention": [
            "Ensure thorough post-harvest vineyard sanitation by discing under fallen leaves.",
            "Canopy management: prune lower suckers to prevent soil-to-leaf spore splashing."
        ]
    },
    "Grape___healthy": {
        "crop": "Grape",
        "condition": "Healthy Grape Foliage",
        "pathogen": "None (Healthy Plant)",
        "type": "Healthy",
        "severity": "None",
        "symptoms": [
            "Lush, deeply lobed emerald-green leaves with supple texture and clean veins.",
            "Strong cane extension and balanced tendril growth without leaf spots or mildew dust."
        ],
        "organic_solutions": [
            "Foliar spray with biological stimulants such as seaweed or fulvic acid."
        ],
        "chemical_solutions": [
            "No chemical fungicides needed."
        ],
        "fertilizer_advice": [
            "Apply balanced vineyard fertilizer or compost based on petiole nutrient analysis.",
            "Maintain soil pH between 6.0 and 6.8 with adequate calcium availability."
        ],
        "prevention": [
            "Maintain proactive canopy management (hedging, leaf pulling around fruit zone).",
            "Monitor vineyard moisture levels and scout weekly for powdery mildew or leafhopper pests."
        ]
    },
    "Potato___Early_blight": {
        "crop": "Potato",
        "condition": "Early Blight",
        "pathogen": "Alternaria solani (Fungus)",
        "type": "Fungal",
        "severity": "Moderate",
        "symptoms": [
            "Dark brown to black spots with concentric rings creating a distinctive target-board pattern.",
            "Yellowing (chlorosis) around lesions; starts on mature bottom leaves and progresses upward.",
            "Leaves dry up, become brittle, and remain hanging on the stem."
        ],
        "organic_solutions": [
            "Spray copper hydroxide or copper octanoate at 7-10 day intervals.",
            "Apply Bacillus subtilis bio-fungicide to colonize leaf surfaces before infection.",
            "Strip off and discard heavily infected lower leaves."
        ],
        "chemical_solutions": [
            "Apply protectant fungicides like Chlorothalonil or Mancozeb before disease spreads.",
            "Use systemic fungicides such as Azoxystrobin, Difenoconazole, or Boscalid if symptoms worsen."
        ],
        "fertilizer_advice": [
            "Maintain steady nitrogen levels; nitrogen deficiency accelerates early blight susceptibility.",
            "Apply potassium sulfate to strengthen epidermal cell walls and tuber storage quality."
        ],
        "prevention": [
            "Use drip irrigation instead of overhead watering to keep potato foliage dry.",
            "Rotate potato fields with non-solanaceous crops (grasses, legumes) for at least 3 years."
        ]
    },
    "Potato___Late_blight": {
        "crop": "Potato",
        "condition": "Late Blight",
        "pathogen": "Phytophthora infestans (Oomycete)",
        "type": "Fungal / Oomycete",
        "severity": "Critical",
        "symptoms": [
            "Large, dark brown to purplish-black water-soaked lesions expanding rapidly on leaves.",
            "White downy fungal-like growth visible on the underside of leaves in humid or dewy conditions.",
            "Rapid rotting, blackening, and foul odor of the entire potato foliage; infects tubers causing dry brown rot."
        ],
        "organic_solutions": [
            "Apply fixed copper or Bordeaux mixture immediately upon local late blight alerts.",
            "Destroy and bury entire infected plants if early isolated focal points appear to protect neighboring crops."
        ],
        "chemical_solutions": [
            "Spray specialized oomycete fungicides: Cymoxanil, Dimethomorph, Mandipropamid, or Metalaxyl.",
            "Follow a strict 5-7 day protective spray schedule during cool (10-20°C), foggy or rainy weather."
        ],
        "fertilizer_advice": [
            "Avoid excessive nitrogen which produces an overly dense canopy that traps moisture.",
            "Ensure adequate phosphorus and calcium to fortify tuber skin resistance."
        ],
        "prevention": [
            "Plant only certified disease-free seed potatoes.",
            "Hill soil high over developing potato tubers to prevent washed-down spores from contacting tubers."
        ]
    },
    "Potato___healthy": {
        "crop": "Potato",
        "condition": "Healthy Potato Foliage",
        "pathogen": "None (Healthy Plant)",
        "type": "Healthy",
        "severity": "None",
        "symptoms": [
            "Full, vigorous, dark-green compound leaves without spots, necrosis, or curling.",
            "Erect, sturdy stems with uniform flowering and healthy tuber formation."
        ],
        "organic_solutions": [
            "Apply preventative foliar sprays of seaweed extract or compost tea."
        ],
        "chemical_solutions": [
            "No chemical fungicides required."
        ],
        "fertilizer_advice": [
            "Side-dress with balanced N-P-K (10-20-20 or 5-10-10) during tuber initiation.",
            "Maintain slightly acidic soil pH between 5.5 and 6.5 to discourage potato scab."
        ],
        "prevention": [
            "Monitor weather conditions for late blight risk warnings.",
            "Maintain consistent hilling and weed control between rows."
        ]
    },
    "Strawberry___Leaf_scorch": {
        "crop": "Strawberry",
        "condition": "Leaf Scorch",
        "pathogen": "Diplocarpon earlianum (Fungus)",
        "type": "Fungal",
        "severity": "Moderate",
        "symptoms": [
            "Numerous irregular purple-to-dark-brown blotches without light centers.",
            "Lesions coalesce causing entire leaf margins to turn brown, curl upward, and look burnt or scorched.",
            "Infected flowers and fruit stems turn brown and die, reducing fruit yield."
        ],
        "organic_solutions": [
            "Apply copper-based fungicides or sulfur before flowers open.",
            "Mow or renovate strawberry beds immediately after harvest to destroy infected foliage."
        ],
        "chemical_solutions": [
            "Apply Captan or Thiophanate-methyl early in the spring as new leaves emerge.",
            "Rotate with Pyraclostrobin (Cabrio) if leaf scorch was severe the prior season."
        ],
        "fertilizer_advice": [
            "Avoid spring applications of high-nitrogen fertilizer; apply fertilizer after post-harvest renovation.",
            "Ensure adequate potassium to maintain water balance in leaf margins."
        ],
        "prevention": [
            "Plant in well-drained soil with full sun exposure and wide row spacing for good air movement.",
            "Use drip irrigation; avoid overhead watering that keeps leaves wet for prolonged hours."
        ]
    },
    "Strawberry___healthy": {
        "crop": "Strawberry",
        "condition": "Healthy Strawberry Foliage",
        "pathogen": "None (Healthy Plant)",
        "type": "Healthy",
        "severity": "None",
        "symptoms": [
            "Glossy trifoliate leaves with vibrant green coloration and crisp serrated borders.",
            "Sturdy runners and robust crown growth without purplish spotting or necrosis."
        ],
        "organic_solutions": [
            "Apply organic mulch (pine needles or clean wheat straw) around plants."
        ],
        "chemical_solutions": [
            "No chemical sprays required."
        ],
        "fertilizer_advice": [
            "Apply balanced organic fertilizer (10-10-10) during planting and post-harvest renovation.",
            "Maintain optimal soil pH (5.8 - 6.5) with rich organic content."
        ],
        "prevention": [
            "Clean dead and yellowing leaves during spring cleanup.",
            "Keep strawberry fruit off bare soil with mulch to prevent ground rots."
        ]
    },
    "Tomato___Bacterial_spot": {
        "crop": "Tomato",
        "condition": "Bacterial Spot",
        "pathogen": "Xanthomonas perforans / vesicatoria (Bacteria)",
        "type": "Bacterial",
        "severity": "High",
        "symptoms": [
            "Small, dark, water-soaked circular spots (<3mm) on leaves that turn brown and necrotic.",
            "Leaves turn yellow, wither, and drop, exposing green tomatoes to sunscald.",
            "Raised, scabby, rough dark spots with white halos on green fruit."
        ],
        "organic_solutions": [
            "Apply copper sulfate or copper octanoate at first sight of lesions.",
            "Use bio-pesticides containing Bacillus subtilis or bacteriophages targeting Xanthomonas."
        ],
        "chemical_solutions": [
            "Spray copper hydroxide combined with Mancozeb (Mancozeb enhances copper bioavailability against resistant strains).",
            "Apply Acibenzolar-S-methyl (Actigard) to activate systemic acquired resistance."
        ],
        "fertilizer_advice": [
            "Avoid heavy nitrogen applications which induce soft vegetative tissues easily invaded by bacteria.",
            "Apply balanced calcium and potassium to enhance plant epidermal toughness."
        ],
        "prevention": [
            "Never work in tomato fields when foliage is wet from rain or morning dew.",
            "Sterilize tomato stakes, ties, and pruning tools with a 10% bleach solution."
        ]
    },
    "Tomato___Early_blight": {
        "crop": "Tomato",
        "condition": "Early Blight",
        "pathogen": "Alternaria linariae / solani (Fungus)",
        "type": "Fungal",
        "severity": "Moderate to High",
        "symptoms": [
            "Dark brown spots with concentric target-like rings surrounded by yellow chlorotic margins.",
            "Begins on lowest, oldest leaves and works upward as the plant matures.",
            "Stem cankers and dark, leathery, sunken spots at the stem end of fruits."
        ],
        "organic_solutions": [
            "Apply copper fungicides or potassium bicarbonate every 7 to 10 days.",
            "Prune bottom 12-18 inches of foliage once plant is established to prevent soil splash."
        ],
        "chemical_solutions": [
            "Spray protective Chlorothalonil or Mancozeb early in the season.",
            "Apply systemic Azoxystrobin, Difenoconazole, or Penthiopyrad if disease spreads."
        ],
        "fertilizer_advice": [
            "Maintain steady soil fertility; stressed or nitrogen-deficient tomato plants succumb faster to early blight.",
            "Ensure adequate calcium and potassium for healthy fruit and foliage vigor."
        ],
        "prevention": [
            "Mulch heavily beneath tomato plants with straw or plastic to prevent rain-splash from soil.",
            "Stake or cage tomato plants to maintain upright, aerated growth."
        ]
    },
    "Tomato___Late_blight": {
        "crop": "Tomato",
        "condition": "Late Blight",
        "pathogen": "Phytophthora infestans (Oomycete)",
        "type": "Fungal / Oomycete",
        "severity": "Critical",
        "symptoms": [
            "Irregular, greasy, water-soaked pale-green to dark brown lesions expanding rapidly.",
            "Delicate white fungal-like sporulation on the underside of leaves in moist weather.",
            "Total foliage collapse within days; large, firm, greasy golden-brown blotches on green fruit."
        ],
        "organic_solutions": [
            "Apply copper hydroxide or Bordeaux mixture at the very first report of regional late blight.",
            "Immediately bag and remove severely infected plants from the garden; do not compost."
        ],
        "chemical_solutions": [
            "Spray specialized oomycete fungicides: Mandipropamid (Revus), Cymoxanil (Curzate), or Dimethomorph.",
            "Maintain tight 5-day protective spray intervals when cool, wet, overcast conditions persist."
        ],
        "fertilizer_advice": [
            "Avoid excessive nitrogen which promotes dense, slow-drying canopies.",
            "Ensure adequate soil aeration and avoid waterlogged roots."
        ],
        "prevention": [
            "Plant late-blight resistant tomato varieties like Mountain Magic, Defiant, or Plum Regal.",
            "Locate tomato plantings away from potato fields and destroy any volunteer potato sprouts."
        ]
    },
    "Tomato___Leaf_Mold": {
        "crop": "Tomato",
        "condition": "Leaf Mold",
        "pathogen": "Passalora fulva (Fungus)",
        "type": "Fungal",
        "severity": "Moderate (Severe in Greenhouses)",
        "symptoms": [
            "Pale green or yellowish spots with diffuse borders on upper leaf surfaces.",
            "Olive-green to velvety brown mold growth directly underneath on the lower leaf surface.",
            "Leaves curl, wither, and drop prematurely, starting from the base of the plant."
        ],
        "organic_solutions": [
            "Apply sulfur or copper fungicides, ensuring thorough coverage on leaf undersides.",
            "Apply bio-fungicides such as Trichoderma harzianum or Bacillus subtilis."
        ],
        "chemical_solutions": [
            "Apply Chlorothalonil or Mancozeb before humidity levels exceed 85%.",
            "In high-tunnel or greenhouse setups, use Cyazofamid or Difenoconazole."
        ],
        "fertilizer_advice": [
            "Maintain balanced fertility; avoid high humidity from excessive transpiration due to over-fertilization.",
            "Ensure sufficient potassium to bolster cell wall integrity."
        ],
        "prevention": [
            "Maximize ventilation in greenhouse/tunnel structures using exhaust fans and horizontal airflow.",
            "Space plants widely and prune suckers to allow rapid drying of foliage."
        ]
    },
    "Tomato___Septoria_leaf_spot": {
        "crop": "Tomato",
        "condition": "Septoria Leaf Spot",
        "pathogen": "Septoria lycopersici (Fungus)",
        "type": "Fungal",
        "severity": "Moderate to High",
        "symptoms": [
            "Numerous small, circular spots (1-3mm) with dark brown margins and white or grayish centers.",
            "Tiny black specks (pycnidia) clearly visible in the light centers of lesions.",
            "Heavy defoliation starting at bottom of plant, leaving stems bare with sunburnt fruit."
        ],
        "organic_solutions": [
            "Apply copper octanoate or sulfur every 7-10 days throughout rainy spells.",
            "Remove and safely dispose of infected lower leaves at first sight."
        ],
        "chemical_solutions": [
            "Spray Chlorothalonil, Mancozeb, or Pyraclostrobin upon first disease detection.",
            "Apply fungicides every 7-14 days until harvest, adhering to pre-harvest intervals."
        ],
        "fertilizer_advice": [
            "Maintain steady nutrition; well-nourished plants produce new foliage faster than disease defoliates.",
            "Provide slow-release organic fertilizers with magnesium and calcium."
        ],
        "prevention": [
            "Do not wet tomato leaves during irrigation; always apply water at the soil line.",
            "Enforce a strict 2-3 year crop rotation away from tomatoes, peppers, and eggplants."
        ]
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "crop": "Tomato",
        "condition": "Two-Spotted Spider Mites",
        "pathogen": "Tetranychus urticae (Arachnid Pest)",
        "type": "Pest",
        "severity": "Moderate to High",
        "symptoms": [
            "Fine yellow, white, or bronze stippling / speckling on upper leaf surfaces.",
            "Delicate silken webbing visible on leaf undersides, growing tips, and flower clusters.",
            "Leaves turn pale, dry, leathery, and drop; severe infestations kill the entire vine."
        ],
        "organic_solutions": [
            "Spray insecticidal soap or neem oil thoroughly covering leaf undersides.",
            "Release predatory mites (Phytoseiulus persimilis or Neoseiulus californicus).",
            "Wash dusty foliage with high-pressure water spray to disrupt mite webbing and breeding."
        ],
        "chemical_solutions": [
            "Apply selective miticides such as Bifenazate (Acramite), Abamectin, or Spiromesifen.",
            "Avoid broad-spectrum pyrethroid insecticides which kill natural beneficial predatory insects."
        ],
        "fertilizer_advice": [
            "Avoid excessive nitrogen fertilization; high nitrogen makes plant sap richer in amino acids, accelerating mite reproduction.",
            "Ensure adequate irrigation as water-stressed plants are preferred by spider mites."
        ],
        "prevention": [
            "Keep garden pathways moist or mulched to suppress dusty conditions favored by mites.",
            "Quarantine and inspect new tomato seedlings before planting out in gardens."
        ]
    },
    "Tomato___Target_Spot": {
        "crop": "Tomato",
        "condition": "Target Spot",
        "pathogen": "Corynespora cassiicola (Fungus)",
        "type": "Fungal",
        "severity": "Moderate",
        "symptoms": [
            "Small, pinpoint brown spots on upper leaf surfaces enlarging into circular lesions with light brown centers.",
            "Concentric rings visible inside mature spots, resembling early blight but without large yellow halos.",
            "Sunken, circular lesions on green and ripe tomato fruit."
        ],
        "organic_solutions": [
            "Apply copper fungicides or bio-fungicides (Bacillus subtilis) at 7-day intervals.",
            "Promptly prune infected leaves from the lower canopy."
        ],
        "chemical_solutions": [
            "Spray Chlorothalonil, Mancozeb, or Azoxystrobin + Difenoconazole.",
            "Rotate with Boscalid or Fluxapyroxad to prevent fungicide resistance."
        ],
        "fertilizer_advice": [
            "Maintain balanced N-P-K fertility; apply adequate potassium to harden plant tissues.",
            "Avoid over-fertilizing with nitrogen which creates excessive dense foliage."
        ],
        "prevention": [
            "Increase plant spacing to at least 24 inches between plants for continuous air circulation.",
            "Prune lower leaves to maintain a 12-inch gap between soil and foliage."
        ]
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "crop": "Tomato",
        "condition": "Tomato Yellow Leaf Curl Virus (TYLCV)",
        "pathogen": "Begomovirus (Whitefly-transmitted Virus)",
        "type": "Viral",
        "severity": "Critical",
        "symptoms": [
            "Severe upward curling and cupping of leaf margins.",
            "Interveinal chlorosis with bright yellow or pale green leaf edges.",
            "Marked stunting of plants with bunched, bushy top growth; flower drop with zero fruit set."
        ],
        "organic_solutions": [
            "Control silverleaf whitefly vectors using yellow sticky traps and insecticidal soap sprays.",
            "Spray horticultural mineral oil or neem oil to deter whiteflies from feeding and transmitting virus.",
            "Immediately pull up, bag, and discard infected virus-harboring plants."
        ],
        "chemical_solutions": [
            "No chemical cure exists for plant viruses; chemical control must target the insect vector (Whitefly).",
            "Apply systemic insecticides like Imidacloprid, Acetamiprid, or Dinotefuran early in the season."
        ],
        "fertilizer_advice": [
            "Infected plants cannot be cured by fertilizer; focus nutrients on healthy neighboring plants.",
            "Apply balanced micronutrients (zinc, iron) to non-infected plants to maximize defense."
        ],
        "prevention": [
            "Plant TYLCV-resistant tomato cultivars (e.g. Tygress, Charger, Red Bounty).",
            "Cover young plants with 50-mesh insect-proof floating row covers until flowering."
        ]
    },
    "Tomato___Tomato_mosaic_virus": {
        "crop": "Tomato",
        "condition": "Tomato Mosaic Virus (ToMV)",
        "pathogen": "Tobamovirus (Mechanically-transmitted Virus)",
        "type": "Viral",
        "severity": "High",
        "symptoms": [
            "Mottling of leaves with alternating light green and dark green mosaic patterns.",
            "Fern-like distortion or blistering of leaves with strap-like, narrowed leaflets.",
            "Stunted plant growth and uneven internal browning (brown wall) of tomato fruit."
        ],
        "organic_solutions": [
            "No cure exists once infected; rogue out and destroy infected plants immediately.",
            "Dip hands and tools in skim milk or a 20% non-fat dry milk solution before pruning (milk proteins neutralize virus transmission)."
        ],
        "chemical_solutions": [
            "No chemical fungicides or viricides are effective against viral infections."
        ],
        "fertilizer_advice": [
            "Do not over-fertilize with nitrogen, which increases symptom severity on infected plants.",
            "Maintain optimal soil pH (6.2 - 6.8) and steady phosphorus for root health."
        ],
        "prevention": [
            "Plant certified virus-resistant varieties marked with TMV or ToMV resistance.",
            "Strictly avoid tobacco use near tomato plants as tobacco products frequently harbor the virus.",
            "Thoroughly sanitize pots, stakes, and greenhouse structures."
        ]
    },
    "Tomato___healthy": {
        "crop": "Tomato",
        "condition": "Healthy Tomato Foliage",
        "pathogen": "None (Healthy Plant)",
        "type": "Healthy",
        "severity": "None",
        "symptoms": [
            "Deep, uniform green foliage with robust leaflets and sturdy glandular stems.",
            "Abundant flower truss development and unblemished growing shoots without spots, curl, or wilting."
        ],
        "organic_solutions": [
            "Apply compost tea or foliar kelp extract every 2 weeks to promote beneficial epiphytic bacteria."
        ],
        "chemical_solutions": [
            "No chemical treatments needed."
        ],
        "fertilizer_advice": [
            "Side-dress with balanced organic fertilizer (e.g. 5-10-10 or tomato-specific formula with calcium).",
            "Maintain regular watering to ensure continuous calcium uptake and prevent blossom end rot."
        ],
        "prevention": [
            "Stake or trellis vines and prune suckers to optimize light interception and air movement.",
            "Keep bottom 12 inches of stems free of leaves to eliminate soil-borne pathogen splash."
        ]
    }
}

os.makedirs("data", exist_ok=True)
with open("data/advisory.json", "w", encoding="utf-8") as f:
    json.dump(advisory, f, indent=2, ensure_ascii=False)

print(f"Successfully generated data/advisory.json with {len(advisory)} classes.")
