use anyhow::Result;
use blockhash::{blockhash16, blockhash256, blockhash64};
use clap::{Parser, ValueEnum};
use std::collections::HashMap;
use std::path::{Path, PathBuf};
use walkdir::{DirEntry, WalkDir};

// use crate::{build_pb, build_status_spinner2, check_ckpt, OrtModel};

#[derive(Parser, Debug)]
pub struct Deduplicator {
    // only focus on the valid images, others will be omitted.
    /// directory about to deal with
    #[arg(short, long, required = true)]
    input: String,

    /// generate report
    #[arg(short, long)]
    output: Option<String>,

    /// doing recursively
    #[arg(short, long)]
    recursive: bool,

    /// methods for dedup
    #[arg(short, long, value_enum, default_value_t = Models::Dinov2s)]
    model: Models,

    /// threshold, similarity
    #[arg(long, default_value_t = 0.9995)]
    thresh: f32,

    /// device id
    #[arg(long, default_value_t = 0)]
    device_id: u32,

    /// move, not copy
    #[arg(short, long)]
    mv: bool,

    /// verbose
    #[arg(short, long)]
    verbose: bool,
}

#[derive(Debug, Clone, ValueEnum)]
enum Models {
    Dinov2s,
    Dinov2b,
}

// impl Deduplicator {
//     pub fn is_hidden(&self, entry: &DirEntry) -> bool {
//         entry
//             .file_name()
//             .to_str()
//             .map(|s| s.starts_with('.'))
//             .unwrap_or(false)
//     }

//     fn fetch_files(&self) -> Vec<PathBuf> {
//         let mut ys = Vec::new();

//         // iteration
//         for entry in WalkDir::new(&self.input)
//             .into_iter()
//             .filter_entry(|e| !self.is_hidden(e))
//         {
//             let entry = entry.unwrap();

//             // directory excluded
//             if entry.file_type().is_dir() {
//                 continue;
//             }

//             // non-recrusive
//             if !self.recursive && entry.depth() > 1 {
//                 continue;
//             }
//             ys.push(entry.path().canonicalize().unwrap());
//         }
//         ys
//     }

//     pub fn run(&self) -> Result<()> {
//         // check inputs
//         assert!(
//             std::path::Path::new(&self.input).exists(),
//             "{}",
//             format!(
//                 "{:?} is not a valid directory or file",
//                 std::path::Path::new(&self.input)
//             )
//         );

//         // load models
//         let pb = build_status_spinner2("Building model...");
//         let model_name = match self.model {
//             Models::Dinov2s => "dinov2_s.onnx",
//             Models::Dinov2b => "dinov2_b.onnx",
//         };
//         // let model_name = "test.onnx";
//         let model_path = check_ckpt(model_name);
//         let extractor = OrtModel::new(model_path.to_str().unwrap(), self.device_id)?;
//         pb.finish_with_message(format!("Done model building => {:?}", pb.elapsed()));

//         // // download with reqwest
//         // download_sth("https://github.com/jamjamjon/assets/releases/download/usls/test.onnx", "/mnt/z/Desktop/test.onnx");

//         // fetch files
//         let pb = build_status_spinner2("Fetching files...");
//         let files = self.fetch_files();
//         pb.finish_with_message(format!("Done files fetching => {:?}", pb.elapsed()));

//         // // build index
//         // let pb = build_status_spinner2("Building index...");
//         // let options = usearch::ffi::IndexOptions {
//         //     dimensions: extractor.n_feats as usize,
//         //     metric: usearch::ffi::MetricKind::IP,
//         //     quantization: usearch::ffi::ScalarKind::F32,
//         //     connectivity: 0,
//         //     expansion_add: 0,
//         //     expansion_search: 0,
//         //     // multi: false,
//         // };
//         // let index = usearch::new_index(&options).unwrap();
//         // pb.finish_with_message(format!("Done index building => {:?}", pb.elapsed()));

//         // build progress spinner
//         let pb = build_pb(files.len() as u64, "De-dup".to_string());

//         // container
//         let mut map_non_duplicated: HashMap<PathBuf, Array<f32, IxDyn>> = HashMap::new();
//         let mut v_duplicates: Vec<PathBuf> = Vec::new();
//         let mut v_others: Vec<PathBuf> = Vec::new(); // save other files or deprecated images

//         // iteration
//         for (_idx, path) in files.iter().enumerate() {
//             pb.inc(1);

//             // try load image
//             let im = match image::io::Reader::open(path) {
//                 Err(_) => {
//                     v_others.push(path.to_path_buf());
//                     continue;
//                 }
//                 Ok(reader) => match reader.with_guessed_format() {
//                     Err(_) => {
//                         v_others.push(path.to_path_buf());
//                         continue;
//                     }
//                     Ok(x) => match x.decode() {
//                         Err(_) => {
//                             v_others.push(path.to_path_buf());
//                             continue;
//                         }
//                         Ok(image) => image,
//                     },
//                 },
//             };

//             // extract feat
//             let feat = extractor.extract(im);

//             // let feat_c = feat.clone();
//             // let feat_c: Vec<_> = feat_c.iter().map(|x| *x).collect();
//             // println!("> last index size {:?}", index.size());
//             // match index.add(idx as u64, &feat_c) {
//             //     Ok(_) => println!("> feats add succeed!"),
//             //     Err(e) => println!("> {:?}", e),
//             // }
//             // let results = index.search(&first, 10).unwrap();

//             // feats matching
//             // TODO: use some crate
//             let mut has_matched = false;
//             for f in map_non_duplicated.values() {
//                 let score = (feat.clone() * f).sum();
//                 // println!("score: {:?}", score);

//                 // save duplicated
//                 if score > self.thresh {
//                     v_duplicates.push(path.to_path_buf());
//                     has_matched = true;
//                     break;
//                 }
//             }

//             // save non-duplicated
//             if !has_matched {
//                 map_non_duplicated.insert(path.to_path_buf(), feat);
//             }
//         }
//         pb.finish();

//         // summary
//         let space_4 = "    ";
//         let cnt_total = files.len();
//         let cnt_dup = v_duplicates.len();
//         let cnt_non_dup = map_non_duplicated.len();
//         let cnt_others = v_others.len();
//         println!(
//             "\n\nSummary:\n\
//             {}directory: {}\n\
//             {}{} duplicates, {} non-duplicates, {} others, {} totals.\n\
//             {}Doing recursively: {}\n\
//             {}Saving results: {}\n",
//             space_4,
//             Path::new(&self.input).canonicalize()?.display(),
//             space_4,
//             cnt_dup,
//             cnt_non_dup,
//             cnt_others,
//             cnt_total,
//             space_4,
//             self.recursive,
//             space_4,
//             self.output.is_some()
//         );

//         // deal with images
//         if let Some(output) = &self.output {
//             if cnt_dup == 0 {
//                 println!("Every image is Ok.");
//                 return Ok(());
//             }

//             // let pbx = build_status_spinner2("Copying files...");
//             let mut saveout = PathBuf::from(output);
//             let output_dups: PathBuf;
//             let output_curated: PathBuf;
//             let output_others: PathBuf;

//             // get stem
//             let saveout_parts: Vec<_> = output.split('/').collect();
//             let saveout_fname = saveout_parts.last().unwrap();

//             let mut dir_cnt = 1;
//             loop {
//                 if !saveout.exists() {
//                     saveout.push("Duplicates");
//                     output_dups = saveout.clone();
//                     saveout.set_file_name("Curated");
//                     output_curated = saveout.clone();
//                     saveout.set_file_name("Others");
//                     output_others = saveout.clone();
//                     std::fs::create_dir_all(&output_curated).unwrap();
//                     std::fs::create_dir_all(&output_dups).unwrap();
//                     std::fs::create_dir_all(&output_others).unwrap();
//                     break;
//                 } else {
//                     saveout.set_file_name(format!("{}-{}", saveout_fname, dir_cnt));
//                     dir_cnt += 1;
//                 }
//             }

//             // copy file for non-duplicates
//             if map_non_duplicated.is_empty() {
//                 std::fs::remove_dir(output_curated)?;
//             } else {
//                 let pb = build_pb(
//                     map_non_duplicated.len() as u64,
//                     if !self.mv {
//                         "Copying non-duplicates".to_string()
//                     } else {
//                         "Moving non-duplicates".to_string()
//                     },
//                 );
//                 for p in map_non_duplicated.keys() {
//                     pb.inc(1);
//                     let filename = p.file_name().unwrap().to_str().unwrap();
//                     let dst = format!(
//                         "{}/{}",
//                         output_curated.canonicalize().unwrap().to_str().unwrap(),
//                         filename
//                     );
//                     // copy or move
//                     if self.mv {
//                         std::fs::rename(p, dst)?;
//                     } else {
//                         std::fs::copy(p, dst)?;
//                     }
//                 }
//                 pb.finish();
//             }

//             // copy file for duplicates
//             if v_duplicates.is_empty() {
//                 std::fs::remove_dir(output_dups)?;
//             } else {
//                 let pb = build_pb(
//                     v_duplicates.len() as u64,
//                     if !self.mv {
//                         "Copying duplicates".to_string()
//                     } else {
//                         "Moving duplicates".to_string()
//                     },
//                 );
//                 for p in v_duplicates {
//                     let filename = p.file_name().unwrap().to_str().unwrap();
//                     let dst = format!(
//                         "{}/{}",
//                         output_dups.canonicalize().unwrap().to_str().unwrap(),
//                         filename
//                     );
//                     // copy or move
//                     if self.mv {
//                         std::fs::rename(p, dst)?;
//                     } else {
//                         std::fs::copy(p, dst)?;
//                     }
//                 }
//                 pb.finish();
//             }

//             // copy file for others
//             if v_others.is_empty() {
//                 std::fs::remove_dir(output_others)?;
//             } else {
//                 let pb = build_pb(
//                     v_others.len() as u64,
//                     if !self.mv {
//                         "Copying others".to_string()
//                     } else {
//                         "Moving others".to_string()
//                     },
//                 );
//                 for p in v_others {
//                     let filename = p.file_name().unwrap().to_str().unwrap();
//                     let dst = format!(
//                         "{}/{}",
//                         output_others.canonicalize().unwrap().to_str().unwrap(),
//                         filename
//                     );
//                     // copy or move
//                     if self.mv {
//                         std::fs::rename(p, dst)?;
//                     } else {
//                         std::fs::copy(p, dst)?;
//                     }
//                 }
//                 pb.finish();
//             }

//             // info
//             saveout.pop();
//             println!(
//                 "{}Results saved at: {}",
//                 space_4,
//                 saveout.canonicalize()?.display()
//             );
//         }

//         Ok(())
//     }
// }
