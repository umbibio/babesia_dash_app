CREATE TABLE bbig_edge_list ( `src` VARCHAR (14), `trg` VARCHAR (14), `srcDesc` VARCHAR (126), `trgDesc` VARCHAR (126) );
CREATE TABLE bbig_expr_all_genes ( `GeneID` VARCHAR (14), `Sample` VARCHAR (18), `expr` FLOAT );
CREATE TABLE bbig_expr_orth_genes ( `GeneID` VARCHAR (12), `Sample` VARCHAR (23), `expr` FLOAT );
CREATE TABLE bbig_mata_data_all_genes ( `Sample` VARCHAR (18), `seurat_clusters` INT, `PC_1` FLOAT, `PC_2` FLOAT, `PC_3` FLOAT, `UMAP_1` FLOAT, `UMAP_2` FLOAT );
CREATE TABLE bbig_mata_data_orth_genes ( `Sample` VARCHAR (23), `pt` FLOAT, `t` FLOAT, `adj.time` FLOAT, `adj.time.idx` INT, `sc1` FLOAT, `sc2` FLOAT, `rep` INT, `spp` VARCHAR (4), `cell.ord` INT, `phase` VARCHAR (2), `PC_1` FLOAT, `PC_2` FLOAT, `PC_3` FLOAT, `UMAP_1` FLOAT, `UMAP_2` FLOAT );
CREATE TABLE bbig_meta_gene_all_genes ( `GeneID` VARCHAR (14) );
CREATE TABLE bbig_meta_gene_orth_genes ( `GeneID` VARCHAR (12) );
CREATE TABLE bbig_node_info ( `GeneID` VARCHAR (14), `degree` INT, `z.score` FLOAT, `ProductDescription` VARCHAR (126), `phase` VARCHAR (2) );
CREATE TABLE bbig_spline_fit_orth_genes ( `GeneID` VARCHAR (12), `t` FLOAT, `expr` FLOAT, `lb` FLOAT, `ub` FLOAT );
CREATE TABLE bbov_edge_list ( `src` VARCHAR (14), `trg` VARCHAR (14), `srcDesc` VARCHAR (126), `trgDesc` VARCHAR (126) );
CREATE TABLE bbov_expr_all_genes ( `GeneID` VARCHAR (14), `Sample` VARCHAR (18), `expr` FLOAT );
CREATE TABLE bbov_expr_orth_genes ( `GeneID` VARCHAR (12), `Sample` VARCHAR (23), `expr` FLOAT );
CREATE TABLE bbov_mata_data_all_genes ( `Sample` VARCHAR (18), `seurat_clusters` INT, `PC_1` FLOAT, `PC_2` FLOAT, `PC_3` FLOAT, `UMAP_1` FLOAT, `UMAP_2` FLOAT );
CREATE TABLE bbov_mata_data_orth_genes ( `Sample` VARCHAR (23), `pt` FLOAT, `t` FLOAT, `adj.time` FLOAT, `adj.time.idx` INT, `sc1` FLOAT, `sc2` FLOAT, `rep` INT, `spp` VARCHAR (4), `cell.ord` INT, `phase` VARCHAR (2), `PC_1` FLOAT, `PC_2` FLOAT, `PC_3` FLOAT, `UMAP_1` FLOAT, `UMAP_2` FLOAT );
CREATE TABLE bbov_meta_gene_all_genes ( `GeneID` VARCHAR (14) );
CREATE TABLE bbov_meta_gene_orth_genes ( `GeneID` VARCHAR (12) );
CREATE TABLE bbov_node_info ( `GeneID` VARCHAR (14), `degree` INT, `z.score` FLOAT, `ProductDescription` VARCHAR (126), `phase` VARCHAR (2) );
CREATE TABLE bbov_spline_fit_orth_genes ( `GeneID` VARCHAR (12), `t` FLOAT, `expr` FLOAT, `lb` FLOAT, `ub` FLOAT );
CREATE TABLE bdiv_cow_edge_list ( `src` VARCHAR (12), `trg` VARCHAR (12), `srcDesc` VARCHAR (149), `trgDesc` VARCHAR (149) );
CREATE TABLE bdiv_cow_expr_all_genes ( `GeneID` VARCHAR (12), `Sample` VARCHAR (18), `expr` FLOAT );
CREATE TABLE bdiv_cow_expr_orth_genes ( `GeneID` VARCHAR (12), `Sample` VARCHAR (27), `expr` FLOAT );
CREATE TABLE bdiv_cow_mata_data_all_genes ( `Sample` VARCHAR (18), `seurat_clusters` INT, `PC_1` FLOAT, `PC_2` FLOAT, `PC_3` FLOAT, `UMAP_1` FLOAT, `UMAP_2` FLOAT );
CREATE TABLE bdiv_cow_mata_data_orth_genes ( `Sample` VARCHAR (27), `pt` FLOAT, `t` FLOAT, `adj.time` FLOAT, `adj.time.idx` INT, `sc1` FLOAT, `sc2` FLOAT, `rep` INT, `spp` VARCHAR (8), `cell.ord` INT, `phase` VARCHAR (2), `PC_1` FLOAT, `PC_2` FLOAT, `PC_3` FLOAT, `UMAP_1` FLOAT, `UMAP_2` FLOAT );
CREATE TABLE bdiv_cow_meta_gene_all_genes ( `GeneID` VARCHAR (12) );
CREATE TABLE bdiv_cow_meta_gene_orth_genes ( `GeneID` VARCHAR (12) );
CREATE TABLE bdiv_cow_node_info ( `GeneID` VARCHAR (12), `degree` INT, `z.score` FLOAT, `ProductDescription` VARCHAR (149), `phase` VARCHAR (2) );
CREATE TABLE bdiv_cow_spline_fit_orth_genes ( `GeneID` VARCHAR (12), `t` FLOAT, `expr` FLOAT, `lb` FLOAT, `ub` FLOAT );
CREATE TABLE bdiv_human_edge_list ( `src` VARCHAR (12), `trg` VARCHAR (12), `srcDesc` VARCHAR (149), `trgDesc` VARCHAR (149) );
CREATE TABLE bdiv_human_expr_all_genes ( `GeneID` VARCHAR (12), `Sample` VARCHAR (18), `expr` FLOAT );
CREATE TABLE bdiv_human_expr_orth_genes ( `GeneID` VARCHAR (12), `Sample` VARCHAR (29), `expr` FLOAT );
CREATE TABLE bdiv_human_mata_data_all_genes ( `Sample` VARCHAR (18), `seurat_clusters` INT, `PC_1` FLOAT, `PC_2` FLOAT, `PC_3` FLOAT, `UMAP_1` FLOAT, `UMAP_2` FLOAT );
CREATE TABLE bdiv_human_mata_data_orth_genes ( `Sample` VARCHAR (29), `pt` FLOAT, `t` FLOAT, `adj.time` FLOAT, `adj.time.idx` INT, `sc1` FLOAT, `sc2` FLOAT, `rep` INT, `spp` VARCHAR (10), `cell.ord` INT, `phase` VARCHAR (2), `PC_1` FLOAT, `PC_2` FLOAT, `PC_3` FLOAT, `UMAP_1` FLOAT, `UMAP_2` FLOAT );
CREATE TABLE bdiv_human_meta_gene_all_genes ( `GeneID` VARCHAR (12) );
CREATE TABLE bdiv_human_meta_gene_orth_genes ( `GeneID` VARCHAR (12) );
CREATE TABLE bdiv_human_node_info ( `GeneID` VARCHAR (12), `degree` INT, `z.score` FLOAT, `ProductDescription` VARCHAR (149), `phase` VARCHAR (2) );
CREATE TABLE bdiv_human_spline_fit_orth_genes ( `GeneID` VARCHAR (12), `t` FLOAT, `expr` FLOAT, `lb` FLOAT, `ub` FLOAT );
CREATE TABLE bmic_expr_all_genes ( `GeneID` VARCHAR (15), `Sample` VARCHAR (18), `expr` FLOAT );
CREATE TABLE bmic_mata_data_all_genes ( `Sample` VARCHAR (18), `seurat_clusters` INT, `PC_1` FLOAT, `PC_2` FLOAT, `PC_3` FLOAT, `UMAP_1` FLOAT, `UMAP_2` FLOAT );
CREATE TABLE bmic_meta_gene_all_genes ( `GeneID` VARCHAR (15) );
