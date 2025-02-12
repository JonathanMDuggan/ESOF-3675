import pandas as pd
from data_viz import get_correlation, get_mean_median_mode, get_variance_std


track_attributes = {
    "_id": "nominal", # ignored from MongoDB
    "name": "nominal",
    "id": "nominal",
    "popularity": "ordinal",
    "video_id": "nominal",
    "video_name": "nominal",
    "view_count": "numerical",
    "like_count": "numerical",
    "comment_count": "numerical",
    "duration_ms": "numerical",
    "release_date": "nominal", # numerical but set to nominal for now
    "release_date_precision": "nominal",
    "explicit": "binary",
    "track_number": "ordinal"
}

artist_attributes = {
    "_id": "nominal", # ignored from MongoDB
    "name": "nominal",
    "id": "nominal",
    "popularity": "ordinal",
    "total_followers": "numerical"
}

album_attributes = {
    "_id": "nominal", # ignored from MongoDB
    "name": "nominal",
    "id": "nominal",
    "popularity": "ordinal",
    "total_tracks": "numerical",
    "release_date": "nominal", # numerical but set to nominal for now
    "release_date_precision": "nominal",
}

def report_stats_for_tracks(tracks_info_extracted):
    nominal_track_attributes = [key for key, value in track_attributes.items() if value == "nominal"]
    ordinal_track_attributes = [key for key, value in track_attributes.items() if value == "ordinal"]
    numerical_track_attributes = [key for key, value in track_attributes.items() if value == "numerical"]
    binary_track_attributes = [key for key, value in track_attributes.items() if value == "binary"]

    print("\nStats for tracks")
    for attribute in numerical_track_attributes:
        if tracks_info_extracted[attribute].dtype == "object":
            tracks_info_extracted[attribute] = pd.to_numeric(tracks_info_extracted[attribute], downcast="float")
        print(f"Stats for {attribute}")
        print(get_mean_median_mode(tracks_info_extracted, attribute, False))
        print(get_variance_std(tracks_info_extracted, attribute, False))
        print(get_correlation(tracks_info_extracted, attribute, "popularity", False))
    print("\n")

    for attribute in ordinal_track_attributes:
        print(f"Stats for {attribute}")
        print(get_mean_median_mode(tracks_info_extracted, attribute, False, ["mean"]))
    print("\n")

    for attribute in binary_track_attributes:
        print(f"Stats for {attribute}")
        print(get_mean_median_mode(tracks_info_extracted, attribute, False, ["mean", "median"]))

def report_stats_for_artists(artists_info_extracted):
    nominal_artist_attributes = [key for key, value in artist_attributes.items() if value == "nominal"]
    ordinal_artist_attributes = [key for key, value in artist_attributes.items() if value == "ordinal"]
    numerical_artist_attributes = [key for key, value in artist_attributes.items() if value == "numerical"]
    binary_artist_attributes = [key for key, value in artist_attributes.items() if value == "binary"]

    print("\nStats for artists")
    for attribute in numerical_artist_attributes:
        if artists_info_extracted[attribute].dtype == "object":
            artists_info_extracted[attribute] = pd.to_numeric(artists_info_extracted[attribute], downcast="float")
        print(f"Stats for {attribute}")
        print(get_mean_median_mode(artists_info_extracted, attribute, False))
        print(get_variance_std(artists_info_extracted, attribute, False))
        print(get_correlation(artists_info_extracted, attribute, "popularity", False))
    print("\n")

    for attribute in ordinal_artist_attributes:
        print(f"Stats for {attribute}")
        print(get_mean_median_mode(artists_info_extracted, attribute, False, ["mean"]))
    print("\n")

    for attribute in binary_artist_attributes:
        print(f"Stats for {attribute}")
        print(get_mean_median_mode(artists_info_extracted, attribute, False, ["mean", "median"]))


def report_stats_for_albums(albums_info_extracted):
    nominal_album_attributes = [key for key, value in album_attributes.items() if value == "nominal"]
    ordinal_album_attributes = [key for key, value in album_attributes.items() if value == "ordinal"]
    numerical_album_attributes = [key for key, value in album_attributes.items() if value == "numerical"]
    binary_album_attributes = [key for key, value in album_attributes.items() if value == "binary"]

    print("\nStats for albums")
    for attribute in numerical_album_attributes:
        if albums_info_extracted[attribute].dtype == "object":
            albums_info_extracted[attribute] = pd.to_numeric(albums_info_extracted[attribute], downcast="float")
        print(f"Stats for {attribute}")
        print(get_mean_median_mode(albums_info_extracted, attribute, False))
        print(get_variance_std(albums_info_extracted, attribute, False))
        print(get_correlation(albums_info_extracted, attribute, "popularity", False))
    print("\n")

    for attribute in ordinal_album_attributes:
        print(f"Stats for {attribute}")
        print(get_mean_median_mode(albums_info_extracted, attribute, False, ["mean"]))
    print("\n")

    for attribute in binary_album_attributes:
        print(f"Stats for {attribute}")
        print(get_mean_median_mode(albums_info_extracted, attribute, False, ["mean", "median"]))
        