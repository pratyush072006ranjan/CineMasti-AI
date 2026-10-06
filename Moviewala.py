from dotenv import load_dotenv
load_dotenv()

import re
import streamlit as st

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate



# PAGE CONFIG

st.set_page_config(
    page_title="CineMasti AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)



# MODEL


@st.cache_resource
def get_model():

    return ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite-preview"
        
    )


model = get_model()



# PROMPT

movie_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are CineMasti AI, an expert Movie & Web Series Information
Extraction Assistant.

The user will provide the name of a movie or web series.

Your job is to provide useful, organized and entertaining information.

IMPORTANT:
Never invent factual information.

If information is unavailable, write:
"Not available"

Return the answer EXACTLY using the following headings.

==================================================
🎬 BASIC INFORMATION
==================================================

Title:
Type:
Release Year:
Release Date:
Language:
Country:
Genre:
Runtime:
Seasons:
Episodes:
Certification / Age Rating:

==================================================
🎭 CAST & CREW
==================================================

Main Cast:

- Actor — Character
- Actor — Character
- Actor — Character
- Actor — Character
- Actor — Character

Director:
Writer:
Producer:
Music Composer:
Production House:

==================================================
⭐ RATINGS & RECEPTION
==================================================

IMDb Rating:
Rotten Tomatoes:
Other Notable Rating:

Audience Reception:
Critics' Reception:

If a rating is unavailable, write "Not available".

==================================================
📖 STORY
==================================================

Plot Summary:

Give a concise, spoiler-free description in 3–5 sentences.

Main Themes:

Mention the important themes explored.

==================================================
😂 MASTI MODE — HINGLISH SUMMARY
==================================================

Give a funny and entertaining summary in HINGLISH.

Rules:

- Use Roman Hindi + English.
- Make it genuinely funny.
- Use relatable Indian humor.
- Use sarcasm and witty observations.
- Make it sound like a friend explaining the movie.
- Avoid excessive slang.
- Do not use offensive or hateful jokes.
- Avoid major spoilers.
- Length: 150–250 words.

Example style:

"Basically bhai, story shuru hoti hai ek aise bande se jiske problems
itni hain ki normal insaan hota toh resignation de deta. Lekin hero hai,
toh obviously problems solve karne ke bajaye aur problems create karega.
Phir entry hoti hai [character] ki, aur yahan se kahani officially
'bhai ye kya ho raha hai?' mode mein chali jaati hai..."

==================================================
🎯 BEST FOR
==================================================

Mention the type of audience who would enjoy this.

Examples:

- Thriller lovers
- Comedy fans
- Sci-fi enthusiasts
- Family audience
- Slow-burn drama lovers

==================================================
⚠️ CONTENT NOTES
==================================================

Violence:
Language:
Sexual Content:
Mature Themes:
Overall Suitability:

==================================================
🔥 VERDICT
==================================================

Verdict:
Watch / Maybe Watch / Skip

One-Line Verdict:

Give a short and witty one-line verdict.

==================================================

IMPORTANT RULES:

1. Never invent information.
2. Use "Not available" when information is unknown.
3. Keep factual information separate from humor.
4. Do not confuse actors and characters.
5. Mention seasons and episodes only for web series.
6. Keep information concise.
7. Hinglish must use Roman Hindi.
8. Keep the Hinglish section funny and conversational.
9. Do not reveal major spoilers.
10. If the title is ambiguous, mention the ambiguity.
11. Never claim that you searched the internet.
12. Return ONLY the requested information.

"""
    ),
    (
        "human",
        "Movie/Web Series Name: {title}"
    )
])



# SESSION STATE


if "result" not in st.session_state:
    st.session_state.result = None

if "title" not in st.session_state:
    st.session_state.title = ""

if "history" not in st.session_state:
    st.session_state.history = []



# SIDEBAR


with st.sidebar:

    st.title("🎬 CineMasti AI")

    st.caption(
        "Movie intelligence with a little Bollywood-style masala."
    )

    st.divider()

    st.subheader("🎯 What you get")

    st.markdown(
        """
        🎬 **Movie Details**

        🎭 **Cast & Crew**

        ⭐ **Ratings & Reception**

        📖 **Story & Themes**

        😂 **Funny Hinglish Summary**

        🎯 **Best For**

        ⚠️ **Content Notes**

        🔥 **Watch Verdict**
        """
    )

    st.divider()

    st.subheader("💡 Pro Tip")

    st.info(
        "Enter the exact movie or web-series name for better results."
    )

    st.divider()

    if st.session_state.history:

        st.subheader("🕘 Recent Searches")

        for item in reversed(st.session_state.history[-5:]):
            st.caption(f"🎞️ {item}")

    st.divider()

    st.caption("Powered by Mistral AI + LangChain")



# HEADER


st.title("🎬 CineMasti AI")

st.markdown(
    """
### Your movie encyclopedia... but with **desi masti**. 🍿

Enter a movie or web-series name and let AI break it down —
**facts, cast, story, ratings, themes and a hilarious Hinglish summary.**
"""
)

st.divider()


# SEARCH AREA


left, center, right = st.columns([1, 3, 1])

with center:

    title_input = st.text_input(
        "🎞️ What are we watching today?",
        placeholder="e.g. Interstellar, 3 Idiots, Stranger Things...",
        label_visibility="visible"
    )

    analyze = st.button(
        "🚀 ANALYZE THIS MASTERPIECE",
        use_container_width=True,
        type="primary"
    )



# QUICK SUGGESTIONS


if not st.session_state.result:

    st.write("### 🍿 Feeling indecisive?")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        if st.button("🚀 Interstellar", use_container_width=True):
            title_input = "Interstellar"
            analyze = True

    with c2:
        if st.button("😂 3 Idiots", use_container_width=True):
            title_input = "3 Idiots"
            analyze = True

    with c3:
        if st.button("🧪 Breaking Bad", use_container_width=True):
            title_input = "Breaking Bad"
            analyze = True

    with c4:
        if st.button("🦇 The Dark Knight", use_container_width=True):
            title_input = "The Dark Knight"
            analyze = True



# ANALYSIS


if analyze:

    if not title_input.strip():

        st.warning(
            "🎬 Bhai, movie ka naam toh batao! "
            "AI hawa mein movie kaise analyze karega? 😂"
        )

    else:

        title = title_input.strip()

        st.session_state.title = title

        if title not in st.session_state.history:
            st.session_state.history.append(title)

        with st.spinner(
            "🍿 Popcorn ready... AI is analyzing the movie..."
        ):

            try:

                final_prompt = movie_prompt.invoke({
                    "title": title
                })

                response = model.invoke(final_prompt)

                if isinstance(response.content, list):

                    result = "\n".join(
                        item.get("text", "")
                        if isinstance(item, dict)
                        else str(item)
                        for item in response.content
                    )

                else:

                    result = str(response.content)

                st.session_state.result = result

                st.rerun()

            except Exception as e:

                st.error(
                    "❌ Something went wrong while contacting Mistral."
                )

                st.exception(e)


# RESULT


if st.session_state.result:

    result = st.session_state.result


    # HELPER FUNCTIONS


    def normalize_result(text):
        """
        Cleans common formatting problems produced by LLMs.
        """

        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        # Remove markdown code fences
        text = re.sub(r"```(?:text|markdown)?", "", text)
        text = text.replace("```", "")

        # Convert repeated separator lines into a simple newline
        text = re.sub(r"={3,}", "\n", text)
        text = re.sub(r"-{5,}", "\n", text)

        # Force important headings onto their own lines.
        headings = [
            "🎬 BASIC INFORMATION",
            "🎭 CAST & CREW",
            "⭐ RATINGS & RECEPTION",
            "📖 STORY",
            "😂 MASTI MODE — HINGLISH SUMMARY",
            "🎯 BEST FOR",
            "⚠️ CONTENT NOTES",
            "🔥 VERDICT",
        ]

        for heading in headings:
            text = re.sub(
                rf"\s*{re.escape(heading)}\s*",
                f"\n\n{heading}\n\n",
                text,
                flags=re.IGNORECASE
            )

        # Remove excessive blank lines
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()


    def get_section(text, start_heading, end_headings):
        """
        Extracts one section from the LLM response.
        """

        start_pattern = rf"{re.escape(start_heading)}"

        start_match = re.search(
            start_pattern,
            text,
            flags=re.IGNORECASE
        )

        if not start_match:
            return ""

        start = start_match.end()

        remaining = text[start:]

        end_positions = []

        for heading in end_headings:

            match = re.search(
                rf"{re.escape(heading)}",
                remaining,
                flags=re.IGNORECASE
            )

            if match:
                end_positions.append(match.start())

        if end_positions:
            end = min(end_positions)
            section = remaining[:end]
        else:
            section = remaining

        return section.strip()


    def clean_section(text):
        """
        Removes formatting noise from extracted sections.
        """

        if not text:
            return ""

        text = re.sub(r"={3,}", "", text)
        text = re.sub(r"-{5,}", "", text)

        # Remove excessive whitespace
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()


    def extract_field(text, field_names):
        """
        Extracts fields even if multiple fields are present
        on the same line.

        Example:
        Director: ABC Writer: XYZ Producer: PQR
        """

        if not text:
            return "Not available"

        fields = "|".join(
            re.escape(field)
            for field in field_names
        )

        pattern = (
            rf"(?:^|\n|\s)"
            rf"({fields})"
            rf"\s*:\s*"
            rf"(.*?)"
            rf"(?=\s+(?:{fields})\s*:|$)"
        )

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE | re.DOTALL
        )

        if match:

            value = match.group(2).strip()

            value = re.sub(
                r"\s+",
                " ",
                value
            )

            return value

        return "Not available"


    def extract_basic_fields(text):
        """
        Extracts important movie information.
        """

        fields = [
            "Title",
            "Type",
            "Release Year",
            "Release Date",
            "Language",
            "Country",
            "Genre",
            "Runtime",
            "Seasons",
            "Episodes",
            "Certification / Age Rating",
        ]

        data = {}

        for field in fields:

            value = extract_field(
                text,
                [field]
            )

            if value != "Not available":

                # Remove unwanted placeholders
                if "[Only for web series]" in value:
                    value = value.replace(
                        "[Only for web series]",
                        ""
                    ).strip()

                if "[Only if applicable]" in value:
                    value = value.replace(
                        "[Only if applicable]",
                        ""
                    ).strip()

            data[field] = value

        return data


    def extract_crew(text):
        """
        Extracts crew information.
        """

        crew_fields = [
            "Director",
            "Writer",
            "Producer",
            "Music Composer",
            "Production House"
        ]

        crew = {}

        for field in crew_fields:

            crew[field] = extract_field(
                text,
                [field]
            )

        return crew


    def extract_content_notes(text):
        """
        Extracts content warning information.
        """

        fields = [
            "Violence",
            "Language",
            "Sexual Content",
            "Mature Themes",
            "Overall Suitability"
        ]

        notes = {}

        for field in fields:

            notes[field] = extract_field(
                text,
                [field]
            )

        return notes


    def extract_verdict(text):

        verdict = extract_field(
            text,
            ["Verdict"]
        )

        one_line = extract_field(
            text,
            ["One-Line Verdict"]
        )

        return verdict, one_line


    
    # NORMALIZE AI RESPONSE
   

    cleaned_result = normalize_result(result)


    # EXTRACT SECTIONS


    basic_text = get_section(
        cleaned_result,
        "🎬 BASIC INFORMATION",
        [
            "🎭 CAST & CREW",
            "⭐ RATINGS & RECEPTION",
            "📖 STORY",
            "😂 MASTI MODE — HINGLISH SUMMARY",
            "🎯 BEST FOR",
            "⚠️ CONTENT NOTES",
            "🔥 VERDICT"
        ]
    )

    cast_text = get_section(
        cleaned_result,
        "🎭 CAST & CREW",
        [
            "⭐ RATINGS & RECEPTION",
            "📖 STORY",
            "😂 MASTI MODE — HINGLISH SUMMARY",
            "🎯 BEST FOR",
            "⚠️ CONTENT NOTES",
            "🔥 VERDICT"
        ]
    )

    rating_text = get_section(
        cleaned_result,
        "⭐ RATINGS & RECEPTION",
        [
            "📖 STORY",
            "😂 MASTI MODE — HINGLISH SUMMARY",
            "🎯 BEST FOR",
            "⚠️ CONTENT NOTES",
            "🔥 VERDICT"
        ]
    )

    story_text = get_section(
        cleaned_result,
        "📖 STORY",
        [
            "😂 MASTI MODE — HINGLISH SUMMARY",
            "🎯 BEST FOR",
            "⚠️ CONTENT NOTES",
            "🔥 VERDICT"
        ]
    )

    masti_text = get_section(
        cleaned_result,
        "😂 MASTI MODE — HINGLISH SUMMARY",
        [
            "🎯 BEST FOR",
            "⚠️ CONTENT NOTES",
            "🔥 VERDICT"
        ]
    )

    best_text = get_section(
        cleaned_result,
        "🎯 BEST FOR",
        [
            "⚠️ CONTENT NOTES",
            "🔥 VERDICT"
        ]
    )

    content_text = get_section(
        cleaned_result,
        "⚠️ CONTENT NOTES",
        [
            "🔥 VERDICT"
        ]
    )

    verdict_text = get_section(
        cleaned_result,
        "🔥 VERDICT",
        []
    )


    # Clean sections

    basic_text = clean_section(basic_text)
    cast_text = clean_section(cast_text)
    rating_text = clean_section(rating_text)
    story_text = clean_section(story_text)
    masti_text = clean_section(masti_text)
    best_text = clean_section(best_text)
    content_text = clean_section(content_text)
    verdict_text = clean_section(verdict_text)



    # HERO


    st.divider()

    st.markdown(
        f"# 🎞️ {st.session_state.title}"
    )

    st.caption(
        "✨ Your cinematic intelligence report is ready."
    )

    st.divider()



# BASIC INFORMATION — FIXED ONLY THIS SECTION


    if basic_text:

        st.subheader("🎬 Movie Intelligence")

        
        # Extract fields robustly, even when the AI puts
        # multiple fields on the same line.
       

        field_names = [
            "Title",
            "Type",
            "Release Year",
            "Release Date",
            "Language",
            "Country",
            "Genre",
            "Runtime",
            "Seasons",
            "Episodes",
            "Certification / Age Rating"
        ]

        field_pattern = "|".join(
            re.escape(field)
            for field in field_names
        )

        matches = list(
            re.finditer(
                rf"({field_pattern})\s*:",
                basic_text,
                flags=re.IGNORECASE
            )
        )

        info = {}

        for i, match in enumerate(matches):

            field = match.group(1).strip()

            start = match.end()

            if i + 1 < len(matches):
                end = matches[i + 1].start()
            else:
                end = len(basic_text)

            value = basic_text[start:end].strip()

            value = re.sub(
                r"\s+",
                " ",
                value
            )

            value = value.strip("-•|")

            info[field.lower()] = value


       
        # Helper
      

        def get_value(field):

            value = info.get(
                field.lower(),
                ""
            )

            if not value:
                return None

            invalid = [
                "not available",
                "not applicable",
                "n/a",
                "na",
                "[only for web series]",
                "[only if applicable]"
            ]

            if value.lower().strip() in invalid:
                return None

            return value


        
        # Fields to display
        

        display_fields = [
            ("Type", "🎞️"),
            ("Release Year", "📅"),
            ("Release Date", "🗓️"),
            ("Genre", "🎭"),
            ("Language", "🗣️"),
            ("Country", "🌍"),
            ("Runtime", "⏱️"),
            ("Seasons", "📺"),
            ("Episodes", "🔢")
        ]


       
        # Create cards
        

        visible_fields = []

        for field, icon in display_fields:

            value = get_value(field)

            if value:

                visible_fields.append(
                    (field, icon, value)
                )


     
        # 4 cards per row
      

        for i in range(
            0,
            len(visible_fields),
            4
        ):

            row = visible_fields[i:i + 4]

            cols = st.columns(4)

            for col, (field, icon, value) in zip(
                cols,
                row
            ):

                with col:

                    with st.container(
                        border=True
                    ):

                        st.caption(
                            f"{icon} {field}"
                        )

                        st.markdown(
                            f"**{value}**"
                        )



        # Certification
 

        certification = get_value(
            "Certification / Age Rating"
        )

        if certification:

            st.caption(
                f"🔞 **Certification:** {certification}"
            )


        st.divider()

   
    # CAST + RATINGS
  

    cast_col, rating_col = st.columns(
        [1.2, 0.8],
        gap="large"
    )



    # CAST & CREW


    with cast_col:

        if cast_text:

            st.subheader("🎭 Cast & Crew")

            # Main cast
            cast_match = re.search(
                r"Main Cast\s*:?(.*?)(?="
                r"Director\s*:|Writer\s*:|Producer\s*:|"
                r"Music Composer\s*:|Production House\s*:|$)",
                cast_text,
                flags=re.IGNORECASE | re.DOTALL
            )

            if cast_match:

                cast_block = cast_match.group(1).strip()

                cast_lines = []

                for line in cast_block.splitlines():

                    line = line.strip()

                    if not line:
                        continue

                    line = re.sub(
                        r"^[-•*]\s*",
                        "",
                        line
                    )

                    cast_lines.append(line)

                if cast_lines:

                    with st.container(border=True):

                        for person in cast_lines:

                            st.markdown(
                                f"🎬 **{person}**"
                            )

            # Crew
            crew = extract_crew(
                cast_text
            )

            crew_items = [
                (key, value)
                for key, value in crew.items()
                if value != "Not available"
            ]

            if crew_items:

                st.markdown("#### 🎥 Behind the Camera")

                for key, value in crew_items:

                    st.markdown(
                        f"**{key}:** {value}"
                    )



    # RATINGS


    with rating_col:

        if rating_text:

            st.subheader("⭐ Ratings & Reception")

            rating_fields = [
                ("IMDb Rating", "⭐"),
                ("Rotten Tomatoes", "🍅"),
                ("Other Notable Rating", "🏆"),
                ("Audience Reception", "👥"),
                ("Critics' Reception", "📝"),
            ]

            for field, icon in rating_fields:

                value = extract_field(
                    rating_text,
                    [field]
                )

                if value != "Not available":

                    with st.container(
                        border=True
                    ):

                        st.markdown(
                            f"### {icon} {field}"
                        )

                        st.write(value)


    st.divider()



    # STORY + THEMES


    if story_text:

        st.subheader("📖 The Story")

        plot = extract_field(
            story_text,
            ["Plot Summary"]
        )

        themes = extract_field(
            story_text,
            ["Main Themes"]
        )

        story_col, theme_col = st.columns(
            [1.5, 1],
            gap="large"
        )

        with story_col:

            with st.container(
                border=True
            ):

                st.markdown(
                    "### 📖 Plot"
                )

                st.write(
                    plot
                )

        with theme_col:

            with st.container(
                border=True
            ):

                st.markdown(
                    "### 🧠 Themes"
                )

                st.write(
                    themes
                )

    st.divider()



    # MASTI MODE


    if masti_text:

        st.subheader(
            "😂 Masti Mode Activated"
        )

        st.caption(
            "Serious movie analysis has temporarily "
            "left the building. Desi commentary incoming."
        )

        with st.container(
            border=True
        ):

            st.markdown(
                "### 🍿 Bhai, sun..."
            )

            st.markdown(
                masti_text
            )

    st.divider()


    # BEST FOR


    if best_text:

        st.subheader(
            "🎯 This One Is For..."
        )

        # Remove heading-like leftovers
        best_clean = re.sub(
            r"^Best For\s*:?",
            "",
            best_text,
            flags=re.IGNORECASE
        ).strip()

        with st.container(
            border=True
        ):

            lines = best_clean.splitlines()

            for line in lines:

                line = line.strip()

                if not line:
                    continue

                line = re.sub(
                    r"^[-•*]\s*",
                    "",
                    line
                )

                st.markdown(
                    f"🎯 {line}"
                )



    # CONTENT NOTES — EQUAL SIZE CARDS


    if content_text:

        st.divider()

        st.subheader(
            "⚠️ Content & Suitability"
        )

        content_notes = extract_content_notes(
            content_text
        )

        note_icons = {
            "Violence": "🥊",
            "Language": "🗣️",
            "Sexual Content": "🔞",
            "Mature Themes": "⚠️",
            "Overall Suitability": "👥"
        }

  
        # Always keep all five categories
   

        note_fields = [
            "Violence",
            "Language",
            "Sexual Content",
            "Mature Themes",
            "Overall Suitability"
        ]

        note_cols = st.columns(
            5,
            gap="medium"
        )

        for col, field in zip(
            note_cols,
            note_fields
        ):

            value = content_notes.get(
                field,
                "Not available"
            )

            icon = note_icons.get(
                field,
                "📌"
            )

            with col:

                with st.container(
                    border=True,
                    height=300
                ):

                    st.markdown(
                        f"### {icon} {field}"
                    )

                    st.write(
                        value
                    )

   
    # VERDICT


    if verdict_text:

        st.divider()

        st.subheader(
            "🔥 Final Verdict"
        )

        verdict, one_line = extract_verdict(
            verdict_text
        )

        verdict_lower = verdict.lower()

        if "watch" == verdict_lower:

            st.success(
                "🍿 WATCH IT!"
            )

        elif "maybe" in verdict_lower:

            st.warning(
                "🤔 MAYBE WATCH"
            )

        elif "skip" in verdict_lower:

            st.error(
                "🚫 SKIP IT"
            )

        else:

            st.info(
                f"🎬 {verdict}"
            )

        if one_line != "Not available":

            with st.container(
                border=True
            ):

                st.markdown(
                    "### 💬 One-Line Verdict"
                )

                st.markdown(
                    f"> {one_line}"
                )



    # COMPLETE ANALYSIS


    st.divider()

    with st.expander(
        "🔍 View Complete AI Analysis"
    ):

        st.markdown(
            cleaned_result
        )



    # NEW SEARCH


    st.divider()

    if st.button(
        "🔄 Analyze Another Movie",
        use_container_width=True,
        type="secondary"
    ):

        st.session_state.result = None
        st.session_state.title = ""

        st.rerun()