# DS 4320 Project 1: NFL Combine Performance as a Predictor for Career Value


```mermaid
erDiagram
    PLAYERS ||--o{ COMBINE_STATS : completes
    PLAYERS ||--o{ PRO_PERFORMANCE : achieves
    PLAYERS ||--|| DRAFT_DETAILS : assigned_to

    PLAYERS {
        string player_id PK
        string name
        string position
        string college
        float height_inches
        float weight_lbs
    }

    COMBINE_STATS {
        string combine_id PK
        string player_id FK
        float forty_yd_dash
        float vertical_jump
        int bench_press_reps
        float broad_jump_inches
        float three_cone_drill
    }

    PRO_PERFORMANCE {
        string performance_id PK
        string player_id FK
        int season_year
        float cav "Career Approximate Value"
        int games_played
        int games_started
    }

    DRAFT_DETAILS {
        string draft_id PK
        string player_id FK
        int draft_year
        int round
        int pick_number
        string nfl_team
    }
    ```
