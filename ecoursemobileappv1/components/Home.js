import { ActivityIndicator, FlatList, Text, View, Image, TouchableOpacity } from "react-native"
import MyStyles from "../styles/MyStyles"
import Apis, { endpoints } from "../configs/Apis";
import { useEffect, useState } from "react";
import { Chip, List, Searchbar } from "react-native-paper";

const Home = () => {
    const [categories, setCategories] = useState([]);
    const [courses, setCourses] = useState([]);
    const [loading, setLoading] = useState([true])
    const [page, setPage] = useState(1);
    const [cateId, setCateId] = useState[null]
    const [kw, setKw] = useState("");

    const loadCates = async () => {
        let res = await Apis.get(endpoints['categories']);
        setCategories(res.data);
    }

    const loadCourses = async () => {
        try {
            setLoading(true);
            let url = `${endpoints['courses']}?page=${page}`;
            if (kw) {
                url = `${url}&q=${kw}`;
            }

            if (cateId) {
                url = `${url}&category_id=${cateId}`;
            }

            let res = await Apis.get(url)
            setCourses(res.data.results);
        } catch {

        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        loadCates();
    }, []);

    useEffect(() => {
        let timer = setTimeout(() => {
            loadCourses();
        }, 500);
        return () => clearTimeout(timer);
    }, [kw, page, cateId]);

    const loadMore = () => {
        
    }

    return (
        <View style={MyStyles.container}>
            <Text style={MyStyles.subject}>E-COURSE ONLINE</Text>

            <View style={[MyStyles.row, MyStyles.wrap]}>
            <TouchableOpacity key={c.id} onPress={() => setCateId(null)}>
                <Chip style={MyStyles.m}  icon="label">All</Chip>
            </TouchableOpacity>

            {categories.map(c => <TouchableOpacity key={c.id} onPress={() => setCateId(c.id)}>
                <Chip style={MyStyles.m}  icon="label">{c.name}</Chip>
            </TouchableOpacity> )}
            </View>

            <Searchbar placeholder="Nhap tim kiem" onChangeText={setKw} value={kw}/>

            {loading && <ActivityIndicator />}

            <FlatList data={courses} renderItem={({item}) => <List.Item key={item.id} title={item.subject} description={item.created_date} left={() => <Image style={MyStyles.avatar} source={{uri: item.image}} key={item.id} />} />} />
        </View>       
    );
}

export default Home;