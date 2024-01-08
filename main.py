import plotly.graph_objects as go
import networkx as nx
import json
from collections import Counter
from liste import MyList
from sozluk import MyDictionary

class User:
    def __init__(self, user_dict):
        self.username = user_dict['username']
        self.name = user_dict.get('name', '')
        self.followers_count = user_dict.get('followers_count', 0)
        self.following_count = user_dict.get('following_count', 0)
        self.language = user_dict.get('language', '')
        self.region = user_dict.get('region', '')
        self.tweets = user_dict.get('tweets', [])
        self.followers_username = user_dict.get('followers_username', [])
        self.following_username = user_dict.get('following_username', [])
        self.interests = user_dict.get('interests', [])

    def __eq__(self, other):
        return self.username == other.username

    def __hash__(self):
        return hash(self.username)

    def update_interests(self, most_common_words):
        self.interests = [word for word, _ in most_common_words]


class MyHashTable:
    def __init__(self, size):
        self.size = size
        self.table = [list() for _ in range(size)]

    def insert(self, key, value):
        index = hash(key) % self.size
        self.table[index].append((key, value))

    def get(self, key):
        index = hash(key) % self.size
        return [user for user, value in self.table[index] if user == key]


class InterestHashTable:
    def __init__(self, size):
        self.size = size
        self.table = [list() for _ in range(size)]

    def insert(self, key, value):
        for interest in key.interests:
            index = hash(interest) % self.size
            self.table[index].append((interest, value))

    def get_users_with_interest(self, interest):
        index = hash(interest) % self.size
        return [user for topic, user in self.table[index] if topic == interest]


# Kullanıcı nesnelerini içeren bir sözlük oluşturun
users_dict = {user['username']: User(user) for user in json.load(open('/home/irem/Desktop/KOÜ/2. '
                                                                      'sınıf/Pro-Lab-3/fake_twitter_users.json', 'r'))}
hash_table = MyHashTable(size=101)
interests_hash_table = InterestHashTable(size=101)

# Aranılan kullanıcı adını alın
desired_username = input("Enter the username you want to search: ")
desired_user = users_dict.get(desired_username)

if desired_user:
    # Kullanıcı bilgilerini yazdır
    print(f"Kullanıcı adı: {desired_user.username}")
    print(f"İsim: {desired_user.name}")
    print(f"Takipçi sayısı: {desired_user.followers_count}")
    print(f"Takip edilen sayısı: {desired_user.following_count}")
    print(f"Dil: {desired_user.language}")
    print(f"Bölge: {desired_user.region}")
    print(f"Tweetler: {desired_user.tweets}")

    # Tweetleri filtrele ve göster
    words_to_remove = ["the", "of", "and", "one", "for", "while", "a", "an", "in", "on", "with", "at", "by", "to", "from", "as", "its"]
    filtered_tweets = [' '.join([word for word in tweet.lower().split() if word not in words_to_remove]) for tweet in desired_user.tweets]
    print('\n'.join(filtered_tweets))

    # Filtrelenmiş tweetleri tek bir string'e birleştir
    all_tweets_text = ' '.join(filtered_tweets)

    # Metni kelimelere bölen
    words = all_tweets_text.split()

    # Her kelimenin frekansını say
    word_freq = Counter(words)

    # En yaygın kelimeleri göster (örneğin, ilk 30)
    most_common_words = word_freq.most_common(2)
    for word, frequency in most_common_words:
        print(f"{word}: {frequency}")

    # Kullanıcının ilgi alanlarını en yaygın kelimelerle güncelle
    desired_user.update_interests(most_common_words)
    print(f"User's interests: {desired_user.interests}")

    # Loop through all users to update their interests and populate the interest hashtable
    for username, user in users_dict.items():
        # Filter and process tweets as you did for the desired user
        filtered_tweets = [' '.join([word for word in tweet.lower().split() if word not in words_to_remove]) for tweet
                           in user.tweets]
        all_tweets_text = ' '.join(filtered_tweets)
        words = all_tweets_text.split()
        word_freq = Counter(words)
        most_common_words = word_freq.most_common(2)  # Update to the top 10 common words
        user.update_interests(most_common_words)  # Update user interests

        # Insert user interests into the InterestHashTable
        interests_hash_table.insert(user, user.username)  # Storing the user with their username

    # Find users with similar interests to the desired user
    if desired_user:
        desired_user_interests = desired_user.interests
        similar_users = set()
        for interest in desired_user_interests:
            users_with_interest = interests_hash_table.get_users_with_interest(interest)
            for username in users_with_interest:
                similar_users.add(username)

        # Remove the desired user from the similar users set
        similar_users.discard(desired_username)

        # Display similar users and their interests
        if similar_users:
            print(f"Similar users for {desired_username}:")
            for username in similar_users:
                user = users_dict[username]
                print(f"\nUsername: {user.username}")
                print(f"Interests: {user.interests}")
        else:
            print("No similar users found.")


def dfs_search(node, keyword):
    if isinstance(node, dict):
        for key, value in node.items():
            if key == 'content' and isinstance(value, str) and keyword in value.lower():
                print("Tweet found:", value)
            else:
                dfs_search(value, keyword)
    elif isinstance(node, list):
        for item in node:
            dfs_search(item, keyword)


# Load JSON data from file
with open('/home/irem/Desktop/KOÜ/2. sınıf/Pro-Lab-3/fake_twitter_users.json', 'r') as file:
    data = json.load(file)


# Call DFS search for tweets containing '#keyword1'
if desired_user:
    keyword_to_search = desired_user.interests[0]  # Extracting the keyword of interest
    tweets_of_desired_user = desired_user.tweets  # Accessing the tweets of the desired user
    dfs_search(tweets_of_desired_user, keyword_to_search)
else:
    print("Desired user not found.")


# Create a function to generate interest reports
def generate_interest_report(user):
    return f"Username: {user.username}\nInterests: {user.interests}\n\n"

# Generate interest reports for all users and write to a text file
with open('/home/irem/Desktop/KOÜ/2. sınıf/Pro-Lab-3/kullanici_ilgi_alanlari.txt', 'w') as file:
    for username, user in users_dict.items():
        report = generate_interest_report(user)
        file.write(report)

""" JSON dosyasını oku ve users listesine doldur
with open('/home/irem/Desktop/KOÜ/2. sınıf/Pro-Lab-3/fake_wout_tweets.json', 'r') as file:
    data = json.load(file)
    users = data  # JSON verisini users listesine ata

# Initialize the graph
G = nx.DiGraph()

batch_size = 1000  # Number of users to process in each batch
total_users = len(users)

for i in range(0, total_users, batch_size):
    batch_users = users[i:i + batch_size]  # Extract a batch of users

    # Add nodes for this batch
    for user in batch_users:
        G.add_node(user['username'])

    # Process edges for this batch
    for user in batch_users:
        for follower in user['followers_username']:
            G.add_edge(follower, user['username'])

        for following in user['following_username']:
            G.add_edge(user['username'], following)

    # Calculate positions for this batch
    pos = nx.spring_layout(G)

    for node, coords in pos.items():
        G.nodes[node]['pos'] = coords

# Grafı Plotly için hazırla
edge_x = []
edge_y = []
for edge in G.edges():
    x0, y0 = G.nodes[edge[0]]['pos']
    x1, y1 = G.nodes[edge[1]]['pos']
    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')

node_x = []
node_y = []
for node in G.nodes():
    x, y = G.nodes[node]['pos']
    node_x.append(x)
    node_y.append(y)

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        colorscale='YlGnBu',
        reversescale=True,
        color=[],
        size=10,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line=dict(width=2)))

# Grafın düğümlerini renklendirme ve bağlantı sayısını belirtme
node_adjacencies = []
node_text = []
for node, adjacencies in enumerate(G.adjacency()):
    node_adjacencies.append(len(adjacencies[1]))
    node_text.append(f'Node: {adjacencies[0]}<br>Connections: {len(adjacencies[1])}')

node_trace.marker.color = node_adjacencies
node_trace.text = node_text

# Grafı oluştur ve görselleştir
fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title='Kullanıcı İlişkileri Grafi',
                    titlefont_size=16,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20, l=5, r=5, t=40),
                    annotations=[dict(
                        text="",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002)],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )

fig.show()"""



# Load data from JSON file
with open('/home/irem/Desktop/KOÜ/2. sınıf/Pro-Lab-3/fake_wout_tweets.json', 'r') as file:
    data = json.load(file)
    users = data  # JSON verisini users listesine ata


# Function to create and show the graph for a specific user
def show_user_graph(username_to_show, users_data):
    # Initialize the graph
    G = nx.DiGraph()

    # Find the user in the data
    user_to_show = next((user for user in users_data if user['username'] == username_to_show), None)

    if user_to_show:
        # Add the user and their connections to the graph
        G.add_node(user_to_show['username'])

        for follower in user_to_show['followers_username']:
            G.add_edge(follower, user_to_show['username'])

        for following in user_to_show['following_username']:
            G.add_edge(user_to_show['username'], following)

        # Calculate positions
        pos = nx.spring_layout(G)

        for node, coords in pos.items():
            G.nodes[node]['pos'] = coords

        # Create edge trace
        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = G.nodes[edge[0]]['pos']
            x1, y1 = G.nodes[edge[1]]['pos']
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')

        # Create node trace
        node_x = [pos[node][0] for node in G.nodes()]
        node_y = [pos[node][1] for node in G.nodes()]

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=True,
                colorscale='YlGnBu',
                reversescale=True,
                color=[],
                size=10,
                colorbar=dict(
                    thickness=15,
                    title='Node Connections',
                    xanchor='left',
                    titleside='right'
                ),
                line=dict(width=2)))

        # Color nodes and set text for each node
        node_adjacencies = []
        node_text = []
        for node, adjacencies in enumerate(G.adjacency()):
            node_adjacencies.append(len(adjacencies[1]))
            node_text.append(f'Node: {adjacencies[0]}<br>Connections: {len(adjacencies[1])}')

        node_trace.marker.color = node_adjacencies
        node_trace.text = node_text

        # Create and display the graph
        fig = go.Figure(data=[edge_trace, node_trace],
                        layout=go.Layout(
                            title=f'Relationship Graph for User: {username_to_show}',
                            titlefont_size=16,
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20, l=5, r=5, t=40),
                            annotations=[dict(
                                text="",
                                showarrow=False,
                                xref="paper", yref="paper",
                                x=0.005, y=-0.002)],
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                        )

        fig.show()
    else:
        print(f"User '{username_to_show}' not found in the data.")


show_user_graph(desired_username, users)
